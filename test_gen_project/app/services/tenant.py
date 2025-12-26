import uuid
from typing import Optional
from sqlalchemy.orm import Session

from app.models.tenant import Tenant
from app.repositories.tenant import TenantRepository
from app.schemas.tenant import TenantCreate, TenantUpdate

class TenantService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = TenantRepository(db)

    def get_tenant_by_id(self, tenant_id: uuid.UUID) -> Optional[Tenant]:
        return self.repository.get_by_id(tenant_id)

    def get_tenant_by_subdomain(self, subdomain: str) -> Optional[Tenant]:
        return self.repository.get_by_subdomain(subdomain)

    def get_all_tenants(self, skip: int = 0, limit: int = 100):
        return self.repository.get_all()[skip : skip + limit]

    def create_tenant(self, tenant_data: TenantCreate) -> Tenant:
        tenant = Tenant(**tenant_data.model_dump())
        return self.repository.create(tenant)

    def update_tenant(self, tenant_id: uuid.UUID, update_data: TenantUpdate) -> Optional[Tenant]:
        return self.repository.update(tenant_id, update_data)
