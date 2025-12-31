from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_current_active_user, RoleChecker, get_user_service
from app.schemas.user import UserResponse, UserUpdate, ChangePasswordRequest
from app.services.user import UserService
from app.services.auth import AuthService
from app.dependencies import get_current_active_user, RoleChecker, get_user_service, get_auth_service

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/me/change-password")
def change_password(
    request: ChangePasswordRequest,
    current_user=Depends(get_current_active_user),
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Change password for the current logged-in user.
    Requires current password for verification.
    """
    if request.new_password != request.confirm_password:
        raise HTTPException(status_code=400, detail="error.passwords_do_not_match")
        
    auth_service.change_password(current_user.id, request.current_password, request.new_password)
    return {"message": "Password updated successfully."}

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=UserResponse)
def update_current_user(
    user_update: UserUpdate,
    current_user=Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update current user profile.
    """
    # Filter out None values
    update_data = user_update.model_dump(exclude_unset=True)
    
    # Prevent users from changing their own role or status via this endpoint
    if "role" in update_data:
        del update_data["role"]
    if "status" in update_data:
        del update_data["status"]
        
    return user_service.update_user(current_user, update_data)

@router.get("", response_model=List[UserResponse], dependencies=[Depends(RoleChecker(["admin"]))])
def read_users(
    skip: int = 0,
    limit: int = 100,
    current_user=Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Get all users for the current tenant.
    Only accessible by users with 'admin' role.
    """
    return user_service.get_users_by_tenant(current_user.tenant_id, skip, limit)

@router.put("/{user_id}", response_model=UserResponse, dependencies=[Depends(RoleChecker(["admin", "super_admin"]))])
def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user=Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
):
    """
    Update a user.
    - Admins can only update users in their own tenant.
    - Super Admins can update any user.
    """
    if current_user.role == "super_admin":
        target_user = user_service.get_user_by_id(user_id)
    else:
        # Ensure target user belongs to same tenant for regular admins
        target_user = user_service.get_user_by_id_and_tenant(user_id, current_user.tenant_id)
        
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")
        
    update_data = user_update.model_dump(exclude_unset=True)
    return user_service.update_user(target_user, update_data)
