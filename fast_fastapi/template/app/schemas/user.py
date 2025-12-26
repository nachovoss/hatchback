from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr
    name: Optional[str] = None
    surname: Optional[str] = None
    role: Optional[str] = "client"
    status: Optional[str] = "active"

class UserCreate(UserBase):
    password: str
    password_confirmation: str
    subdomain: str  # tenant_subdomain of client

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    tenant_id: UUID
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
