from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Literal, Optional

class AdminBase(BaseModel):
    full_name: str
    position: str
    contact_number: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str
    role: Optional[Literal["admin"]] = "admin"  # Only allow creating regular admins

class Admin(AdminBase):
    id: str  # MongoDB uses string IDs
    role: Literal["superadmin", "admin"]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AdminList(BaseModel):
    """Schema for listing admins"""
    id: str
    full_name: str
    position: str
    email: str
    role: Literal["superadmin", "admin"]
    created_at: datetime
