import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Database
    database_url: str = os.getenv("database_url", "sqlite:///./diabetes.db")

    # JWT
    secret_key: str = os.getenv("secret_key", "your-super-secret-key-change-this-in-production-12345678901234567890")
    algorithm: str = os.getenv("algorithm", "HS256")
    access_token_expire_minutes: int = int(os.getenv("access_token_expire_minutes", "30"))

    # CORS
    cors_origins_str: str = os.getenv("cors_origins_str", "http://localhost:3000,http://localhost:5173")
    cors_origins: list = [origin.strip() for origin in cors_origins_str.split(",")]

# Create a global settings instance
settings = Settings()
