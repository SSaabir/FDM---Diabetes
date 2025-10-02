"""
Prediction Schemas
Pydantic models for diabetes prediction API
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional
from enum import Enum

class GenderEnum(str, Enum):
    male = "male"
    female = "female"
    other = "other"

class ActivityLevelEnum(str, Enum):
    low = "low"
    moderate = "moderate"
    high = "high"

class BloodPressureEnum(str, Enum):
    normal = "normal"
    elevated = "elevated"
    high = "high"

class CholesterolEnum(str, Enum):
    normal = "normal"
    borderline = "borderline"
    high = "high"

class FamilyHistoryEnum(str, Enum):
    yes = "yes"
    no = "no"
    unknown = "unknown"

class SmokingEnum(str, Enum):
    yes = "yes"
    no = "no"
    former = "former"

class PredictionRequest(BaseModel):
    """Request model for diabetes risk prediction - supports dual model system"""
    
    age: int = Field(..., ge=18, le=120, description="Age in years")
    gender: GenderEnum = Field(..., description="Gender")
    height: float = Field(..., ge=100, le=250, description="Height in centimeters")
    weight: float = Field(..., ge=30, le=300, description="Weight in kilograms")
    familyHistory: FamilyHistoryEnum = Field(..., description="Family history of diabetes")
    physicalActivity: ActivityLevelEnum = Field(..., description="Physical activity level")
    smoking: SmokingEnum = Field(..., description="Smoking status")
    bloodPressure: BloodPressureEnum = Field(..., description="Blood pressure level")
    cholesterol: CholesterolEnum = Field(..., description="Cholesterol level")
    
    # Additional field for women-specific model
    gestationalHistory: Optional[bool] = Field(False, description="History of gestational diabetes (for women)")

    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 120:
            raise ValueError('Age must be between 18 and 120')
        return v

    @validator('height')
    def validate_height(cls, v):
        if v < 100 or v > 250:
            raise ValueError('Height must be between 100 and 250 cm')
        return v

    @validator('weight')
    def validate_weight(cls, v):
        if v < 30 or v > 300:
            raise ValueError('Weight must be between 30 and 300 kg')
        return v
    
    @validator('gestationalHistory')
    def validate_gestational_history(cls, v, values):
        # Only relevant for females
        if values.get('gender') == 'female':
            return v if v is not None else False
        return False  # Default to False for non-females

    class Config:
        json_schema_extra = {
            "example": {
                "age": 35,
                "gender": "female",
                "height": 165,
                "weight": 65,
                "familyHistory": "no",
                "physicalActivity": "moderate",
                "smoking": "no",
                "bloodPressure": "normal",
                "cholesterol": "normal",
                "gestationalHistory": False
            }
        }

class PredictionResponse(BaseModel):
    """Response model for diabetes risk prediction - includes dual model info"""
    
    risk_percentage: float = Field(..., description="Diabetes risk percentage (0-100)")
    risk_level: str = Field(..., description="Risk level: low, moderate, or high")
    risk_color: str = Field(..., description="Color code for UI: green, orange, or red")
    recommendations: List[str] = Field(..., description="Personalized health recommendations")
    bmi: float = Field(..., description="Calculated BMI")
    model_used: str = Field(..., description="ML model used for prediction")
    confidence: str = Field(..., description="Prediction confidence: low, moderate, or high")
    
    # Additional fields for dual model system
    gender_detected: Optional[str] = Field(None, description="Detected gender for model routing")
    gestationalHistory: Optional[bool] = Field(None, description="Gestational diabetes history considered")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_percentage": 25.5,
                "risk_level": "low",
                "risk_color": "green",
                "recommendations": [
                    "🍎 Maintain a balanced, healthy diet",
                    "🏃‍♀️ Continue regular physical activity",
                    "📊 Monitor your health annually"
                ],
                "bmi": 26.1,
                "model_used": "General Model",
                "confidence": "high",
                "gender_detected": "female",
                "gestationalHistory": False
            }
        }

class ModelInfoResponse(BaseModel):
    """Response model for ML model information"""
    
    rf_model_loaded: bool = Field(..., description="Whether Random Forest model is loaded")
    feature_columns_loaded: bool = Field(..., description="Whether feature columns are loaded")
    scaler_loaded: bool = Field(..., description="Whether feature scaler is loaded")
    total_features: int = Field(..., description="Number of features in the model")
    model_type: str = Field(..., description="Type of ML model")
    version: str = Field(..., description="Model version")

class ValidationResponse(BaseModel):
    """Response model for input validation"""
    
    valid: bool = Field(..., description="Whether the input is valid")
    errors: List[str] = Field(..., description="List of validation errors")
    calculated_bmi: Optional[float] = Field(None, description="Calculated BMI if height/weight provided")
    warnings: List[str] = Field(..., description="List of warnings")