from app.main import create_application

# Create the FastAPI application
app = create_application()

# For development, you can run this with: uvicorn main:app --reload
# Updated: Using compressed ML models for production deployment 