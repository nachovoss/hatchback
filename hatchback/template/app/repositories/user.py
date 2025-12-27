from uuid import UUID
from app.models.user import User
from app.repositories.base import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, db):
        super().__init__(db, User)

    def get_by_username(self, username: str):
        return self.db.query(self.model).filter(self.model.username == username).first()

    def get_by_username_and_tenant(self, username: str, tenant_id: UUID):
        return (
            self.db.query(self.model)
            .filter(self.model.username == username, self.model.tenant_id == tenant_id)
            .first()
        )

    def get_by_email(self, email: str):
        return self.db.query(self.model).filter(self.model.email == email).first()

    def get_by_email_and_tenant(self, email: str, tenant_id: UUID):
        return (
            self.db.query(self.model)
            .filter(self.model.email == email, self.model.tenant_id == tenant_id)
            .first()
        )

    def get_by_username_or_email_and_tenant(
        self, username: str, email: str, tenant_id: UUID
    ):
        return (
            self.db.query(self.model)
            .filter(
                ((self.model.username == username) | (self.model.email == email))
                & (self.model.tenant_id == tenant_id)
            )
            .first()
        )

    def get_by_id_and_tenant(self, user_id: UUID, tenant_id: UUID):
        return (
            self.db.query(self.model)
            .filter(self.model.id == user_id, self.model.tenant_id == tenant_id)
            .first()
        )

    def get_all_by_tenant(self, tenant_id: UUID, skip: int = 0, limit: int = 100):
        return (
            self.db.query(self.model)
            .filter(self.model.tenant_id == tenant_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
