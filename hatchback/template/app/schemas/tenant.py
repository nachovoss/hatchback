from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

class TenantBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    subdomain: str = Field(..., min_length=3, max_length=63, pattern="^[a-z0-9-]+$")
    domain: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = True

class TenantCreate(TenantBase):
    pass

class TenantPublic(BaseModel):
    """Schema for public tenant information (safe to expose)"""
    id: UUID
    name: str
    subdomain: str
    
    model_config = ConfigDict(from_attributes=True)

class TenantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    subdomain: Optional[str] = Field(None, min_length=3, max_length=63, pattern="^[a-z0-9-]+$")
    domain: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class TenantResponse(TenantBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
