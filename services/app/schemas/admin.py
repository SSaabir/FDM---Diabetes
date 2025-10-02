from pydantic import BaseModel, EmailStr
from datetime import datetime

class AdminBase(BaseModel):
    full_name: str
    position: str
    contact_number: str
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

class Admin(AdminBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
