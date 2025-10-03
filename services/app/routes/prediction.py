"""
Prediction API Routes
Handles diabetes risk prediction requests
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from typing import Any
import logging
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..services.prediction import prediction_service
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..utils.auth import get_current_user
from ..models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

# Create limiter instance
limiter = Limiter(key_func=get_remote_address)

# -------------------------------
# ✅ Sanitization helper
# -------------------------------
def sanitize_input(field: str, value: Any) -> Any:
    if isinstance(value, str):
        value = value.strip().replace("<", "").replace(">", "")
        if field in ['age', 'height', 'weight', 'bloodPressure', 'cholesterol', 'hbA1c_level', 'blood_glucose_level']:
            value = ''.join(c for c in value if c.isdigit() or c == '.')
            try:
                value = float(value)
            except ValueError:
                value = 0.0
        if field == 'gender':
            value = value.lower()
            if value not in ['male', 'female', 'other']:
                value = ''
        if field in ['smoking', 'physicalActivity', 'familyHistory']:
            value = value.lower()
    if isinstance(value, (int, float)):
        return value
    return value

# -------------------------------
# ✅ Public Predict diabetes risk (no auth required)
# -------------------------------
@router.post("/predict-public", response_model=PredictionResponse)
@limiter.limit("30/minute")  # Increased from 10/minute
async def predict_diabetes_risk_public(
    request: Request,
    prediction_request: PredictionRequest
):
    try:
        user_input = prediction_request.dict()
        for field in user_input:
            user_input[field] = sanitize_input(field, user_input[field])
        prediction_result = prediction_service.predict_diabetes_risk(user_input)
        logger.info(f"Public prediction: {prediction_result['risk_level']} risk")
        return PredictionResponse(**prediction_result)
    except ValueError as e:
        logger.error(f"Public prediction error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in public prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

# -------------------------------
# ✅ Predict diabetes risk (authenticated)
# -------------------------------
@router.post("/predict", response_model=PredictionResponse)
@limiter.limit("20/minute")  # Increased from 5/minute
async def predict_diabetes_risk(
    request: Request,
    prediction_request: PredictionRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        user_input = prediction_request.dict()
        for field in user_input:
            user_input[field] = sanitize_input(field, user_input[field])
        prediction_result = prediction_service.predict_diabetes_risk(user_input)
        logger.info(f"Prediction for user {current_user.id}: {prediction_result['risk_level']} risk")
        return PredictionResponse(**prediction_result)
    except ValueError as e:
        logger.error(f"Prediction error for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in prediction for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

# -------------------------------
# ✅ Get model information
# -------------------------------
@router.get("/model-info")
@limiter.limit("5/minute")
async def get_model_info(request: Request):
    try:
        model_info = {
            "rf_model_loaded": prediction_service.rf_model is not None,
            "feature_columns_loaded": prediction_service.feature_columns is not None,
            "scaler_loaded": prediction_service.scaler is not None,
            "total_features": len(prediction_service.feature_columns) if prediction_service.feature_columns else 0,
            "model_type": "Random Forest Classifier",
            "version": "1.0"
        }
        return model_info
    except Exception as e:
        logger.error(f"Error retrieving model info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving model information")

# -------------------------------
# ✅ Validate input only
# -------------------------------
@router.post("/validate-input")
@limiter.limit("5/minute")
async def validate_prediction_input(
    request: Request,
    prediction_request: PredictionRequest,
    current_user: User = Depends(get_current_user)
):
    try:
        user_input = prediction_request.dict()
        for field in user_input:
            user_input[field] = sanitize_input(field, user_input[field])
        validation_errors = []
        age = user_input.get('age')
        if age and (age < 18 or age > 120):
            validation_errors.append("Age must be between 18 and 120")
        height = user_input.get('height')
        if height and (height < 100 or height > 250):
            validation_errors.append("Height must be between 100 and 250 cm")
        weight = user_input.get('weight')
        if weight and (weight < 30 or weight > 300):
            validation_errors.append("Weight must be between 30 and 300 kg")
        bmi = None
        if height and weight:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            if bmi < 15 or bmi > 50:
                validation_errors.append("Calculated BMI is outside normal range (15-50)")
        return {
            "valid": len(validation_errors) == 0,
            "errors": validation_errors,
            "calculated_bmi": round(bmi, 1) if bmi else None,
            "warnings": []
        }
    except Exception as e:
        logger.error(f"Error validating input: {str(e)}")
        raise HTTPException(status_code=500, detail="Error validating input")

@router.get("/debug/models")
async def debug_models():
    """Debug endpoint to check model files and loading status"""
    from pathlib import Path
    import os
    
    try:
        models_path = Path(__file__).parent.parent.parent / "models"
        
        # Check model files
        model_files = {}
        model_files_to_check = [
            "diabetes_general_model.pkl",
            "diabetes_general_model_compressed_lvl3.pkl", 
            "diabetes_women_model.pkl",
            "diabetes_model.pkl",
            "diabetes_rf_tuned.pkl",
            "general_model_features.json",
            "women_model_features.json"
        ]
        
        for file_name in model_files_to_check:
            file_path = models_path / file_name
            if file_path.exists():
                size_mb = file_path.stat().st_size / (1024 * 1024)
                model_files[file_name] = {
                    "exists": True,
                    "size_mb": round(size_mb, 2),
                    "path": str(file_path)
                }
            else:
                model_files[file_name] = {
                    "exists": False,
                    "size_mb": 0,
                    "path": str(file_path)
                }
        
        # Check prediction service status
        service_status = {
            "general_model_loaded": prediction_service.general_model is not None,
            "women_model_loaded": prediction_service.women_model is not None,
            "legacy_model_loaded": prediction_service.rf_model is not None,
            "general_model_type": str(type(prediction_service.general_model)) if prediction_service.general_model else None,
            "women_model_type": str(type(prediction_service.women_model)) if prediction_service.women_model else None,
            "legacy_model_type": str(type(prediction_service.rf_model)) if prediction_service.rf_model else None
        }
        
        return {
            "models_path": str(models_path),
            "models_path_exists": models_path.exists(),
            "model_files": model_files,
            "service_status": service_status,
            "environment": os.environ.get("RAILWAY_ENVIRONMENT", "local")
        }
        
    except Exception as e:
        return {
            "error": str(e),
            "models_path": "unknown",
            "models_path_exists": False,
            "model_files": {},
            "service_status": {},
            "environment": os.environ.get("RAILWAY_ENVIRONMENT", "local")
        }
