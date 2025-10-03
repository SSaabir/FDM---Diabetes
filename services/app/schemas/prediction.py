"""
Prediction Schemas - Simplified Version
Pydantic models for diabetes prediction API
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class PredictionRequest(BaseModel):
    """Simplified request model for diabetes risk prediction"""
    
    age: int = Field(..., ge=18, le=120, description="Age in years")
    gender: str = Field(..., description="Gender (male/female)")
    height: float = Field(..., ge=100, le=250, description="Height in centimeters")
    weight: float = Field(..., ge=30, le=300, description="Weight in kilograms")
    family_history: bool = Field(False, description="Family history of diabetes")
    physical_activity: float = Field(2.5, ge=0, le=10, description="Physical activity hours per week")
    smoking_history: str = Field("never", description="Smoking history")
    hypertension: bool = Field(False, description="Has hypertension")
    heart_disease: bool = Field(False, description="Has heart disease")
    sleep_hours: float = Field(7.5, ge=4, le=12, description="Sleep hours per night")
    diet_pattern: str = Field("balanced", description="Diet pattern")
    alcohol_intake: str = Field("none", description="Alcohol consumption level")
    medication_use: bool = Field(False, description="Currently using medication")
    stress_level: str = Field("moderate", description="Stress level")

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

    class Config:
        json_schema_extra = {
            "example": {
                "age": 35,
                "gender": "male",
                "height": 175,
                "weight": 80,
                "family_history": False,
                "physical_activity": 3.0,
                "smoking_history": "never",
                "hypertension": False,
                "heart_disease": False,
                "sleep_hours": 7.5,
                "diet_pattern": "balanced",
                "alcohol_intake": "none",
                "medication_use": False,
                "stress_level": "moderate"
            }
        }

class PredictionResponse(BaseModel):
    """Simplified response model for diabetes risk prediction"""
    
    risk_probability: float = Field(..., description="Diabetes risk probability (0-1)")
    risk_level: str = Field(..., description="Risk level: Low, Moderate, or High")
    recommendations: List[str] = Field(..., description="Health recommendations")
    bmi: float = Field(..., description="Calculated BMI")
    model_used: str = Field(..., description="Model used for prediction")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_probability": 0.25,
                "risk_level": "Low",
                "recommendations": [
                    "Maintain a healthy lifestyle",
                    "Regular exercise and balanced diet",
                    "Annual health checkups"
                ],
                "bmi": 26.1,
                "model_used": "Random Forest Model"
            }
        }