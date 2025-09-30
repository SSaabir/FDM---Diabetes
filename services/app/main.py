from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes.auth import router as auth_router
from .routes.prediction import router as prediction_router
from .routes.chat import router as chat_router
from .routes.metrics import router as metrics_router

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Diabetes Prediction API",
        description="Backend API for Diabetes Prediction System",
        version="1.0.0",
    )

    # Set up CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router, prefix="/auth", tags=["authentication"])
    app.include_router(prediction_router, prefix="/api", tags=["prediction"])
    app.include_router(chat_router, prefix="/api", tags=["chat"])
    app.include_router(metrics_router, prefix="/api", tags=["metrics"])

    @app.get("/")
    async def root():
        return {"message": "Diabetes Prediction API is running!"}

    return app
