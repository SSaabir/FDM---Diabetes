from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import func

from ..database import get_db
from ..models.user import User
from ..schemas.metrics import MetricsResponse, TrainingJobs

router = APIRouter()

@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(db: Session = Depends(get_db)):
    try:
        # Count total users
        total_users = db.query(func.count(User.id)).scalar()

        # Count active users today (based on updated_at field)
        today = date.today()
        active_today = db.query(func.count(User.id)).filter(
            func.date(User.updated_at) == today
        ).scalar()

        # Stub values (replace with actual ML job tracking later)
        model_accuracy = 0.847  # Example, 84.7%
        training_jobs = TrainingJobs(active=1, completed=2)

        return MetricsResponse(
            totalUsers=total_users or 0,
            activeToday=active_today or 0,
            modelAccuracy=model_accuracy,
            trainingJobs=training_jobs
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {str(e)}")
