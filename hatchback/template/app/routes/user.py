from typing import List
from fastapi import APIRouter, Depends
from app.dependencies import get_current_active_user, RoleChecker, get_user_service
from app.schemas.user import UserResponse
from app.services.user import UserService

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserResponse)
def read_current_user(current_user=Depends(get_current_active_user)):
    return current_user

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
