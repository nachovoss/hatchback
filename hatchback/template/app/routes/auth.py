from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request

from app.dependencies import (
    get_auth_service,
    get_tenant_service,
    get_user_service,
)
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RegisterResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from app.schemas.user import UserCreate
from app.services.auth import AuthService
from app.services.tenant import TenantService
from app.services.user import UserService
from app.config.limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=RegisterResponse)
@limiter.limit("5/minute")
def register_user(
    request: Request,
    user: UserCreate,
    user_service: UserService = Depends(get_user_service),
    auth_service: AuthService = Depends(get_auth_service),
    tenant_service: TenantService = Depends(get_tenant_service),
):
    tenant = tenant_service.get_tenant(user.tenant_id)
    if not tenant or not tenant.is_active:
        raise HTTPException(
            status_code=400,
            detail=f"error.invalid_tenant_id '{user.tenant_id}' or tenant is not active",
        )

    if user.password != user.password_confirmation:
        raise HTTPException(
            status_code=400, detail="error.password_and_confirmation_do_not_match"
        )
    new_user = user_service.create_user(
        user.username,
        user.email,
        user.password,
        tenant,
        user.name,
        user.surname,
        user.role
    )
    token_data = {
        "id": str(new_user.id),
        "tenant_id": str(new_user.tenant_id),
        "username": new_user.username,
        "email": new_user.email,
        "role": new_user.role,
    }
    access_token = auth_service.create_access_token(
        data=token_data
    )
    return {
        "user": new_user,
        "token": {"access_token": access_token, "token_type": "bearer"},
    }

@router.post("/login", response_model=LoginResponse)
@limiter.limit("5/minute")
async def login(
    request: Request,
    login_request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
    tenant_service: TenantService = Depends(get_tenant_service),
):
    tenant = tenant_service.get_tenant(login_request.tenant_id)
    if not tenant or not tenant.is_active:
        raise HTTPException(
            status_code=400,
            detail=f"error.invalid_tenant_id '{login_request.tenant_id}' or tenant is not active",
        )

    user_data = auth_service.authenticate_user(
        login_request.username, login_request.password, tenant.id
    )
    if not user_data:
        raise HTTPException(
            status_code=401,
            detail="error.invalid_credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(
        data=user_data
    )
    return {
        "user": user_data,
        "token": {"access_token": access_token, "token_type": "bearer"},
    }


@router.post("/forgot-password")
@limiter.limit("3/minute")
async def forgot_password(
    request: Request,
    forgot_request: ForgotPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
    tenant_service: TenantService = Depends(get_tenant_service),
):
    tenant = tenant_service.get_tenant(forgot_request.tenant_id)
    if not tenant or not tenant.is_active:
        raise HTTPException(
            status_code=400,
            detail=f"error.invalid_tenant_id '{forgot_request.tenant_id}' or tenant is not active",
        )

    auth_service.forgot_password(forgot_request.email, tenant.id)
    return {"message": "If the email exists, a password recovery email has been sent."}


@router.post("/reset-password")
@limiter.limit("3/minute")
async def reset_password(
    request: Request,
    reset_request: ResetPasswordRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    if reset_request.new_password != reset_request.confirm_password:
        raise HTTPException(
            status_code=400, detail="error.passwords_do_not_match"
        )

    auth_service.reset_password(reset_request.token, reset_request.new_password)
    return {"message": "Password has been reset successfully."}
