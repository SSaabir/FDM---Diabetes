from datetime import datetime, date
from typing import Optional
from beanie import Document
from pydantic import EmailStr, Field
from pymongo import IndexModel

class User(Document):
    email: EmailStr = Field(..., unique=True)
    password_hash: str
    full_name: str
    phone: Optional[str] = None
    date_of_birth: Optional[str] = None  # Changed to string for better MongoDB compatibility
    address: Optional[str] = None
    bio: Optional[str] = None
    avatar: Optional[str] = None  # URL to avatar image
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"  # Collection name
        indexes = [
            IndexModel("email", unique=True),
            "full_name",
            "created_at"
        ]
