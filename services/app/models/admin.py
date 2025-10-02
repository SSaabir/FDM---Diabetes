from datetime import datetime
from beanie import Document
from pydantic import EmailStr, Field
from pymongo import IndexModel
from typing import Literal

class Admin(Document):
    full_name: str
    position: str
    contact_number: str
    email: EmailStr = Field(..., unique=True)
    password_hash: str
    role: Literal["superadmin", "admin"] = Field(default="admin")  # Role-based access
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "admins"
        indexes = [
            IndexModel("email", unique=True),
            "position",
            "role",
            "created_at"
        ]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
