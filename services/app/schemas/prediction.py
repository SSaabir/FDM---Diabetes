"""
Prediction Schemas - Simplified Version
Pydantic models for diabetes prediction API
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional

class PredictionRequest(BaseModel):
    """Enhanced request model for diabetes risk prediction with optional clinical data"""
    
    # Required basic fields
    age: int = Field(..., ge=18, le=120, description="Age in years")
    gender: str = Field(..., description="Gender (male/female)")
    height: float = Field(..., ge=100, le=250, description="Height in centimeters")
    weight: float = Field(..., ge=30, le=300, description="Weight in kilograms")
    
    # Health history
    familyHistory: str = Field("no", description="Family history of diabetes (yes/no/unknown)")
    gestationalHistory: str = Field("no", description="History of gestational diabetes (yes/no)")
    hypertension: str = Field("no", description="Hypertension history (yes/no)")
    heartDisease: str = Field("no", description="Heart disease history (yes/no)")
    medicationUse: str = Field("no", description="Current medication use (yes/no)")
    
    # Lifestyle factors
    physicalActivity: str = Field("moderate", description="Physical activity level")
    smoking: str = Field("never", description="Smoking history")
    sleepHours: int = Field(7, ge=4, le=12, description="Sleep hours per night")
    dietPattern: str = Field("balanced", description="Diet pattern")
    alcoholIntake: str = Field("none", description="Alcohol consumption level")
    
    # Optional clinical data - these are the key additions
    hbA1c: Optional[float] = Field(None, ge=3.0, le=15.0, description="HbA1c level in % (optional)")
    bloodGlucose: Optional[float] = Field(None, ge=50, le=500, description="Blood glucose level in mg/dL (optional)")

    @validator('gestationalHistory')
    def validate_gestational_history(cls, v):
        if v.lower() not in ['yes', 'no']:
            raise ValueError('Gestational history must be "yes" or "no"')
        return v.lower()

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

    @validator('hbA1c')
    def validate_hba1c(cls, v):
        if v is not None and (v < 3.0 or v > 15.0):
            raise ValueError('HbA1c must be between 3.0 and 15.0%')
        return v

    @validator('bloodGlucose')
    def validate_glucose(cls, v):
        if v is not None and (v < 50 or v > 500):
            raise ValueError('Blood glucose must be between 50 and 500 mg/dL')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "age": 35,
                "gender": "male",
                "height": 175,
                "weight": 80,
                "familyHistory": "no",
                "gestationalHistory": "no",
                "hypertension": "no", 
                "heartDisease": "no",
                "medicationUse": "no",
                "physicalActivity": "moderate",
                "smoking": "never",
                "sleepHours": 7,
                "dietPattern": "balanced",
                "alcoholIntake": "none",
                "hbA1c": 5.7,
                "bloodGlucose": 95
            }
        }

class PredictionResponse(BaseModel):
    """Enhanced response model for diabetes risk prediction"""
    
    risk_percentage: float = Field(..., description="Diabetes risk percentage (0-100)")
    risk_level: str = Field(..., description="Risk level: low, moderate, or high")
    recommendations: List[str] = Field(..., description="Health recommendations")
    bmi: float = Field(..., description="Calculated BMI")
    model_used: str = Field(..., description="Model used for prediction")
    confidence: Optional[str] = Field(None, description="Confidence level based on available data")
    has_clinical_data: bool = Field(..., description="Whether clinical data was provided")

    class Config:
        json_schema_extra = {
            "example": {
                "risk_percentage": 25.0,
                "risk_level": "low",
                "recommendations": [
                    "Maintain a healthy lifestyle",
                    "Regular exercise and balanced diet",
                    "Annual health checkups"
                ],
                "bmi": 26.1,
                "model_used": "Clinical Model (HbA1c + Lifestyle)",
                "confidence": "high",
                "has_clinical_data": True
            }
        }