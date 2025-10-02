from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Dict, Any, List

from ..models.admin import Admin as AdminModel
from ..schemas.admin import AdminCreate, Admin, AdminList
from ..utils.auth import create_access_token, get_current_admin
from ..utils.security import get_password_hash, verify_password
from ..config import settings

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")  # Changed to use unified login

def convert_admin_to_schema(db_admin: AdminModel) -> Dict[str, Any]:
    """Convert MongoDB Admin document to Pydantic schema format"""
    return {
        "id": str(db_admin.id),
        "full_name": db_admin.full_name,
        "position": db_admin.position,
        "contact_number": db_admin.contact_number,
        "email": db_admin.email,
        "role": db_admin.role,
        "created_at": db_admin.created_at,
        "updated_at": db_admin.updated_at
    }

async def require_superadmin(current_admin: AdminModel = Depends(get_current_admin)):
    """Ensure current admin is a superadmin"""
    if current_admin.role != "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superadmin can perform this action"
        )
    return current_admin

@router.get("/me", response_model=Admin)
async def get_current_admin_info(current_admin: AdminModel = Depends(get_current_admin)):
    """Get current admin information"""
    admin_data = convert_admin_to_schema(current_admin)
    return Admin(**admin_data)

@router.post("/create-admin", response_model=Admin)
async def create_admin(
    admin_data: AdminCreate,
    current_admin = Depends(require_superadmin)
):
    """Create a new admin (only superadmin can do this)"""
    
    # Check if admin already exists
    existing_admin = await AdminModel.find_one(AdminModel.email == admin_data.email)
    if existing_admin:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(admin_data.password)
    
    # Create new admin (always as regular admin, not superadmin)
    new_admin = AdminModel(
        full_name=admin_data.full_name,
        position=admin_data.position,
        contact_number=admin_data.contact_number,
        email=admin_data.email,
        password_hash=hashed_password,
        role="admin"  # Force regular admin role
    )
    await new_admin.insert()
    
    # Convert to response format
    admin_response = convert_admin_to_schema(new_admin)
    return Admin(**admin_response)

@router.get("/list-admins", response_model=List[AdminList])
async def list_admins(current_admin: AdminModel = Depends(require_superadmin)):
    """List all admins (only superadmin can do this)"""
    
    admins = await AdminModel.find_all().to_list()
    
    admin_list = []
    for admin in admins:
        admin_list.append(AdminList(
            id=str(admin.id),
            full_name=admin.full_name,
            position=admin.position,
            email=admin.email,
            role=admin.role,
            created_at=admin.created_at
        ))
    
    return admin_list

@router.delete("/delete-admin/{admin_id}")
async def delete_admin(
    admin_id: str,
    current_admin: AdminModel = Depends(require_superadmin)
):
    """Delete an admin (only superadmin can do this)"""
    
    # Find the admin to delete
    admin_to_delete = await AdminModel.get(admin_id)
    if not admin_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin not found"
        )
    
    # Prevent superadmin from deleting themselves
    if admin_to_delete.id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )
    
    # Prevent deleting other superadmins
    if admin_to_delete.role == "superadmin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete another superadmin"
        )
    
    await admin_to_delete.delete()
    return {"message": "Admin deleted successfully"}

@router.get("/stats")
async def get_admin_stats(current_admin: AdminModel = Depends(get_current_admin)):
    """Get admin statistics"""
    
    if current_admin.role == "superadmin":
        # Superadmin can see all stats
        total_admins = await AdminModel.count()
        superadmin_count = await AdminModel.find(AdminModel.role == "superadmin").count()
        regular_admin_count = await AdminModel.find(AdminModel.role == "admin").count()
        
        return {
            "total_admins": total_admins,
            "superadmin_count": superadmin_count,
            "regular_admin_count": regular_admin_count,
            "your_role": current_admin.role
        }
    else:
        # Regular admin gets limited stats
        return {
            "your_role": current_admin.role,
            "permissions": ["view_own_profile", "basic_dashboard_access"]
        }
