"""
Prediction API Routes - Simplified Version
Handles diabetes risk prediction requests
"""
from fastapi import APIRouter, HTTPException, Depends
import logging

from ..services.prediction import DiabetesPredictionService
from ..schemas.prediction import PredictionRequest, PredictionResponse
from ..utils.auth import get_current_user
from ..models.user import User

router = APIRouter()
logger = logging.getLogger(__name__)

# Initialize prediction service
prediction_service = DiabetesPredictionService()

@router.get("/version")
async def get_version():
    """Get API version"""
    return {
        "version": "2.0.0-clean",
        "status": "clean restart version"
    }

@router.post("/predict", response_model=PredictionResponse)
async def predict_diabetes_risk(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Predict diabetes risk based on user input
    Requires authentication
    """
    try:
        logger.info(f"Prediction request from user: {current_user.email}")
        
        # Convert request to dict
        user_input = request.dict()
        
        # Get prediction
        result = prediction_service.predict_diabetes_risk(user_input)
        
        # Check for errors
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        logger.info(f"Prediction successful: {result['risk_level']} risk")
        
        return PredictionResponse(**result)
        
    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/health")
async def health_check():
    """Check if prediction service is working"""
    try:
        # Test with sample data
        test_input = {
            "age": 30,
            "gender": "male",
            "height": 175,
            "weight": 70,
            "family_history": False,
            "physical_activity": 3.0,
            "smoking_history": "never",
            "hypertension": False,
            "heart_disease": False,
            "sleep_hours": 8,
            "diet_pattern": "balanced",
            "alcohol_intake": "none",
            "medication_use": False,
            "stress_level": "low"
        }
        
        result = prediction_service.predict_diabetes_risk(test_input)
        
        return {
            "status": "healthy",
            "model_loaded": prediction_service.model is not None,
            "test_prediction": result["risk_level"]
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "model_loaded": False
        }