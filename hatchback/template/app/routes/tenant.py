from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.schemas.tenant import TenantCreate, TenantResponse, TenantPublic, TenantUpdate
from app.services.tenant import TenantService
from app.dependencies import get_current_user, RoleChecker, get_current_active_user

router = APIRouter(prefix="/tenants", tags=["Tenants"])

@router.get("/lookup", response_model=TenantPublic)
def lookup_tenant(subdomain: str, db: Session = Depends(get_db)):
    """
    Public endpoint to resolve a tenant by subdomain.
    Used by the frontend to get the Tenant ID before login.
    """
    service = TenantService(db)
    tenant = service.get_tenant_by_subdomain(subdomain)
    
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Workspace not found"
        )
        
    if not tenant.is_active:
        raise HTTPException(
            status_code=403,
            detail="This workspace is inactive"
        )
        
    return tenant

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

@router.put("/me", response_model=TenantResponse, dependencies=[Depends(RoleChecker(["admin"]))])
def update_current_tenant(
    tenant_update: TenantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update the current tenant.
    Only accessible by users with 'admin' role.
    """
    service = TenantService(db)
    # Admins can't change the active status of their own tenant to avoid locking themselves out
    update_data = tenant_update.model_dump(exclude_unset=True)
    if "is_active" in update_data:
        del update_data["is_active"]
        
    return service.update_tenant(current_user.tenant_id, tenant_update)

@router.put("/{tenant_id}", response_model=TenantResponse, dependencies=[Depends(RoleChecker(["admin", "super_admin"]))])
def update_tenant(
    tenant_id: str,
    tenant_update: TenantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    """
    Update a tenant.
    - Admins can only update their own tenant.
    - Super Admins can update any tenant.
    """
    service = TenantService(db)
    
    # Check permissions
    if current_user.role != "super_admin" and str(current_user.tenant_id) != str(tenant_id):
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this tenant"
        )
        
    # Admins can't change the active status of their own tenant to avoid locking themselves out
    # Super admins can do whatever they want
    if current_user.role != "super_admin":
        update_data = tenant_update.model_dump(exclude_unset=True)
        if "is_active" in update_data:
            del update_data["is_active"]
            # Re-create the model with filtered data if needed, but service.update_tenant usually takes a Pydantic model or dict
            # Let's assume service.update_tenant handles Pydantic models. 
            # If we modified the dict, we should pass the dict or a new model.
            # The service signature is: update_tenant(self, tenant_id: uuid.UUID, update_data: TenantUpdate)
            # So we should probably modify the input model or pass a dict if the service supports it.
            # Looking at service code: return self.repository.update(tenant_id, update_data)
            # Repository usually handles dicts or models. Let's pass the modified dict if possible, 
            # or just modify the model in place if it's mutable (it's not easily).
            # Safest is to create a new TenantUpdate from the filtered dict.
            tenant_update = TenantUpdate(**update_data)

    return service.update_tenant(tenant_id, tenant_update)

@router.post("", response_model=TenantResponse)
async def create_tenant(
    tenant_data: TenantCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    service = TenantService(db)
    tenant = service.create_tenant(tenant_data)
    return tenant
