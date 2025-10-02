# Import all models here to ensure they are registered with SQLAlchemy
from .user import User
from .admin import Admin

__all__ = ["User", "Admin"]
