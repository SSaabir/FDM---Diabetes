from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .routes.auth import router as auth_router

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

    @app.get("/")
    async def root():
        return {"message": "Diabetes Prediction API is running!"}

    return app
