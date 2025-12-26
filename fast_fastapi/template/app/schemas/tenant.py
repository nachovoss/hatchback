from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class TenantBase(BaseModel):
    name: str
    subdomain: str
    domain: Optional[str] = None
    is_active: Optional[bool] = True

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    subdomain: Optional[str] = None
    domain: Optional[str] = None
    is_active: Optional[bool] = None

class TenantResponse(TenantBase):
    id: UUID
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
