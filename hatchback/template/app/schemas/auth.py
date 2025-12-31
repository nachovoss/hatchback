from uuid import UUID
from pydantic import BaseModel, Field
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
