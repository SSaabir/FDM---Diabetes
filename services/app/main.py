from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from .config import settings
from .database import init_database, close_database, health_check
from .routes.auth import router as auth_router
from .routes.prediction import router as prediction_router
from .routes.chat import router as chat_router
from .routes.admin import router as admin_router

# Create limiter
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan with MongoDB initialization"""
    # Startup
    await init_database()
    yield
    # Shutdown
    await close_database()

def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Diabetes Prediction API",
        description="Backend API for Diabetes Prediction System",
        version="1.0.0",
        lifespan=lifespan
    )

    # Attach limiter to app state
    app.state.limiter = limiter

    # Handle rate limit errors globally
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Too Many Requests. Slow down!"}
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
    app.include_router(admin_router, prefix="/admin", tags=["admins"])

    @app.get("/")
    async def root():
        return {"message": "Diabetes Prediction API is running!"}

    @app.get("/health/database")
    async def database_health():
        """Check database connection status"""
        try:
            is_healthy = await health_check()
            if is_healthy:
                return {"status": "healthy", "database": "connected"}
            else:
                return {"status": "degraded", "database": "disconnected", "message": "Running in offline mode"}
        except Exception as e:
            return {"status": "unhealthy", "database": "error", "error": str(e)}

    return app
