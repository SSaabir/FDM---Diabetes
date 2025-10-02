from datetime import timedelta, datetime
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any, Union

from ..models.user import User as UserModel
from ..models.admin import Admin as AdminModel
from ..schemas.user import UserCreate, User, UserLogin, Token, UserProfileUpdate, PasswordChange
from ..utils.auth import create_access_token, verify_token, get_current_user
from ..utils.security import get_password_hash, verify_password
from ..config import settings

router = APIRouter()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def check_database_availability():
    """Check if database is available for auth operations"""
    from ..database import get_database
    database = await get_database()
    if database is None:  # Fixed: Use 'is None' instead of 'not database'
        raise HTTPException(
            status_code=503,
            detail="Authentication service temporarily unavailable. Database connection required."
        )
    return database

def convert_user_to_schema(db_user: UserModel) -> Dict[str, Any]:
    """Convert MongoDB User document to Pydantic schema format"""
    return {
        "id": str(db_user.id),
        "email": db_user.email,
        "full_name": db_user.full_name,
        "phone": db_user.phone,
        "date_of_birth": db_user.date_of_birth,
        "address": db_user.address,
        "bio": db_user.bio,
        "avatar": db_user.avatar,
        "created_at": db_user.created_at,
        "updated_at": db_user.updated_at
    }

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    """Register a new user"""
    # Check database availability
    await check_database_availability()
    
    try:
        # Check if user already exists
        existing_user = await UserModel.find_one(UserModel.email == user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password
        hashed_password = get_password_hash(user.password)
        
        # Create new user
        db_user = UserModel(
            email=user.email,
            password_hash=hashed_password,
            full_name=user.full_name,
            phone=user.phone,
            date_of_birth=user.date_of_birth
        )
        await db_user.insert()
        
        # Convert to response format
        user_data = convert_user_to_schema(db_user)
        return User(**user_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Registration failed: {e}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/signup", response_model=User)
async def signup(user: UserCreate):
    """Alias for register endpoint"""
    return await register(user)

@router.post("/login")
async def unified_login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Unified login for both users and admins"""
    # Check database availability first
    await check_database_availability()
    
    try:
        # First, try to find as a regular user
        user = await UserModel.find_one(UserModel.email == form_data.username)
        if user and verify_password(form_data.password, user.password_hash):
            # Create access token for user
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = create_access_token(
                data={"sub": user.email, "user_type": "user"}, 
                expires_delta=access_token_expires
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_type": "user",
                "user_info": {
                    "id": str(user.id),
                    "email": user.email,
                    "full_name": user.full_name
                }
            }
        
        # If not found as user, try to find as admin
        admin = await AdminModel.find_one(AdminModel.email == form_data.username)
        if admin and verify_password(form_data.password, admin.password_hash):
            # Create access token for admin
            access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
            access_token = create_access_token(
                data={"sub": admin.email, "user_type": "admin"}, 
                expires_delta=access_token_expires
            )
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user_type": "admin",
                "user_info": {
                    "id": str(admin.id),
                    "email": admin.email,
                    "full_name": admin.full_name,
                    "role": admin.role,
                    "position": admin.position
                }
            }
        
        # If neither user nor admin found, raise authentication error
        logger.warning(f"❌ Failed login attempt for: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Login failed due to database error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service temporarily unavailable"
        )

@router.get("/me", response_model=User)
async def read_users_me(current_user: UserModel = Depends(get_current_user)):
    """Get current user information"""
    user_data = convert_user_to_schema(current_user)
    return User(**user_data)

@router.get("/profile", response_model=User)
async def get_user_profile(current_user: UserModel = Depends(get_current_user)):
    """Get detailed user profile information"""
    user_data = convert_user_to_schema(current_user)
    return User(**user_data)

@router.put("/profile", response_model=User)
async def update_user_profile(
    profile_data: UserProfileUpdate,
    current_user: UserModel = Depends(get_current_user)
):
    """Update user profile information (full name, phone, date of birth only)"""
    try:
        # Update only the fields that are provided and allowed
        update_data = {}
        if profile_data.full_name is not None:
            update_data["full_name"] = profile_data.full_name
        if profile_data.phone is not None:
            update_data["phone"] = profile_data.phone
        if profile_data.date_of_birth is not None:
            update_data["date_of_birth"] = profile_data.date_of_birth
        
        # Update the updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        # Update the user in the database
        await current_user.update({"$set": update_data})
        
        # Fetch the updated user
        updated_user = await UserModel.get(current_user.id)
        if not updated_user:
            raise HTTPException(status_code=404, detail="User not found after update")
        
        user_data = convert_user_to_schema(updated_user)
        return User(**user_data)
        
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )

@router.put("/change-password")
async def change_password(
    password_data: PasswordChange,
    current_user: UserModel = Depends(get_current_user)
):
    """Change user password"""
    try:
        # Verify current password
        if not verify_password(password_data.current_password, current_user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Validate new password
        if len(password_data.new_password) < 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New password must be at least 6 characters long"
            )
        
        # Hash new password
        new_password_hash = get_password_hash(password_data.new_password)
        
        # Update password in database
        update_data = {
            "password_hash": new_password_hash,
            "updated_at": datetime.utcnow()
        }
        
        await current_user.update({"$set": update_data})
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error changing password: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )
