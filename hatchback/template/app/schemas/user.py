from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: EmailStr
    name: Optional[str] = Field(None, max_length=100)
    surname: Optional[str] = Field(None, max_length=100)
    role: Optional[str] = "client"
    status: Optional[str] = "active"

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)
    password_confirmation: str = Field(..., min_length=8, max_length=100)
    subdomain: str = Field(..., min_length=3, max_length=63, pattern="^[a-z0-9-]+$") # tenant_subdomain of client

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=50, pattern="^[a-zA-Z0-9_-]+$")
    email: Optional[EmailStr] = None
    name: Optional[str] = Field(None, max_length=100)
    surname: Optional[str] = Field(None, max_length=100)
    password: Optional[str] = Field(None, min_length=8, max_length=100)

class UserResponse(UserBase):
    id: UUID
    tenant_id: UUID
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
