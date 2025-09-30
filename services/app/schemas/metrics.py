from pydantic import BaseModel, Field
from typing import Optional

class TrainingJobs(BaseModel):
    active: int = Field(..., description="Number of active training jobs")
    completed: int = Field(..., description="Number of completed training jobs today")

class MetricsResponse(BaseModel):
    totalUsers: int = Field(..., description="Total registered users")
    activeToday: int = Field(..., description="Users active today")
    modelAccuracy: float = Field(..., description="ML model accuracy (0-1)")
    trainingJobs: TrainingJobs = Field(..., description="Training jobs statistics")

    class Config:
        json_schema_extra = {
            "example": {
                "totalUsers": 12547,
                "activeToday": 1823,
                "modelAccuracy": 0.847,
                "trainingJobs": {"active": 1, "completed": 2}
            }
        }
