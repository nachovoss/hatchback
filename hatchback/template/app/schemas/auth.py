from uuid import UUID
from pydantic import BaseModel, EmailStr, Field
from .user import UserResponse

class LoginRequest(BaseModel):
    username: str
    password: str
    tenant_id: UUID

class Token(BaseModel):
    access_token: str
    token_type: str

class RegisterResponse(BaseModel):
    user: UserResponse
    token: Token

class LoginResponse(BaseModel):
    user: UserResponse
    token: Token

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    tenant_id: UUID

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str
