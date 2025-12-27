from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.tenant import TenantCreate, TenantResponse
from app.services.tenant import TenantService
from app.dependencies import get_current_user

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.get("", response_model=List[TenantResponse])
async def get_all_tenants(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = TenantService(db)
    tenants = service.get_all_tenants(skip, limit)
    return tenants

@router.post("", response_model=TenantResponse)
async def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = TenantService(db)
    tenant = service.create_tenant(tenant_data)
    return tenant
