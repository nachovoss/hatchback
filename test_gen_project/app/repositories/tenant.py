from uuid import UUID
from app.models.tenant import Tenant
from app.repositories.base import BaseRepository

class TenantRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, Tenant)

    def get_by_subdomain(self, subdomain: str):
        return self.db.query(self.model).filter(self.model.subdomain == subdomain).first()

    def get_by_name(self, name: str):
        return self.db.query(self.model).filter(self.model.name == name).first()
