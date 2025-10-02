from datetime import datetime, timedelta, timezone
from typing import Optional, Union
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..config import settings
from ..models.user import User
from ..models.admin import Admin

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        user_type: str = payload.get("user_type", "user")  # Default to user for backward compatibility
        if email is None:
            raise credentials_exception
        return email, user_type
    except JWTError:
        raise credentials_exception

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current authenticated user (regular user only)"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        email, user_type = verify_token(credentials.credentials, credentials_exception)
        
        # Ensure this is a regular user, not an admin
        if user_type != "user":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User access required"
            )
            
        user = await User.find_one(User.email == email)
        if user is None:
            raise credentials_exception
        return user
    except Exception:
        raise credentials_exception

async def get_current_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Get current authenticated admin"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        email, user_type = verify_token(credentials.credentials, credentials_exception)
        
        # Ensure this is an admin, not a regular user
        if user_type != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required"
            )
            
        admin = await Admin.find_one(Admin.email == email)
        if admin is None:
            raise credentials_exception
        return admin
    except Exception as e:
        raise credentials_exception

async def get_current_user_or_admin(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Union[User, Admin]:
    """Get current authenticated user or admin"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        email, user_type = verify_token(credentials.credentials, credentials_exception)
        
        if user_type == "admin":
            admin = await Admin.find_one(Admin.email == email)
            if admin is None:
                raise credentials_exception
            return admin
        else:
            user = await User.find_one(User.email == email)
            if user is None:
                raise credentials_exception
            return user
    except Exception:
        raise credentials_exception
