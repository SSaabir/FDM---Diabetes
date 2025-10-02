import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
# Get the directory of this file and go up one level to find .env
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path, override=True)

class Settings:
    # MongoDB Configuration
    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    database_name: str = os.getenv("DATABASE_NAME", "fdm_diabetes_db")

    # JWT - Fixed environment variable names
    secret_key: str = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production-12345678901234567890")
    algorithm: str = os.getenv("ALGORITHM", "HS256")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    # CORS - Fixed environment variable name
    cors_origins_str: str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")
    cors_origins: list = [origin.strip() for origin in cors_origins_str.split(",")]

    # Groq API Configuration for Diabetes Health Chat
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    groq_model: str = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# Create a global settings instance
settings = Settings()
