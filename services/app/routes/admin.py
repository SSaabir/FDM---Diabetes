from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.admin import Admin as AdminModel
from ..schemas.admin import AdminCreate, Admin
from ..utils.auth import create_access_token, verify_token
from ..utils.security import get_password_hash, verify_password
from ..config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate admin credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    email = verify_token(token, credentials_exception)
    admin = db.query(AdminModel).filter(AdminModel.email == email).first()
    if admin is None:
        raise credentials_exception
    return admin

@router.post("/signup", response_model=Admin)
def signup(admin: AdminCreate, db: Session = Depends(get_db)):
    db_admin = db.query(AdminModel).filter(AdminModel.email == admin.email).first()
    if db_admin:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(admin.password)
    db_admin = AdminModel(
        full_name=admin.full_name,
        position=admin.position,
        contact_number=admin.contact_number,
        email=admin.email,
        password_hash=hashed_password,
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(AdminModel).filter(AdminModel.email == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": admin.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=Admin)
def read_admins_me(current_admin: Admin = Depends(get_current_admin)):
    return current_admin
