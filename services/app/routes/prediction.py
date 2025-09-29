"""
Prediction API Routes
Handles diabetes risk prediction requests
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
import logging

from ..database import get_db
from ..services.prediction import prediction_service
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..utils.auth import get_current_user
from ..models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/predict", response_model=PredictionResponse)
async def predict_diabetes_risk(
    prediction_request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Predict diabetes risk based on user health data
    """
    try:
        # Convert request to dictionary
        user_input = prediction_request.dict()
        
        # Get prediction from ML service
        prediction_result = prediction_service.predict_diabetes_risk(user_input)
        
        # Log prediction for monitoring (without sensitive data)
        logger.info(f"Prediction generated for user {current_user.id}: {prediction_result['risk_level']} risk")
        
        # TODO: Optionally save prediction to database for history
        
        return PredictionResponse(**prediction_result)
        
    except ValueError as e:
        logger.error(f"Prediction error for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    
    except Exception as e:
        logger.error(f"Unexpected error in prediction for user {current_user.id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during prediction")

@router.get("/model-info")
async def get_model_info():
    """
    Get information about the loaded ML models (public endpoint)
    """
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
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail="Error retrieving model information")

@router.post("/validate-input")
async def validate_prediction_input(
    prediction_request: PredictionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Validate prediction input without running the actual prediction
    """
    try:
        # Convert request to dictionary
        user_input = prediction_request.dict()
        
        # Validate input ranges
        validation_errors = []
        
        # Age validation
        age = user_input.get('age')
        if age and (age < 18 or age > 120):
            validation_errors.append("Age must be between 18 and 120")
        
        # Height validation (cm)
        height = user_input.get('height')
        if height and (height < 100 or height > 250):
            validation_errors.append("Height must be between 100 and 250 cm")
        
        # Weight validation (kg)
        weight = user_input.get('weight')
        if weight and (weight < 30 or weight > 300):
            validation_errors.append("Weight must be between 30 and 300 kg")
        
        # Calculate BMI if height and weight provided
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