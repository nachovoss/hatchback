from typing import Optional
from uuid import UUID
import bcrypt
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UserRepository(db)

    def get_user_by_id(self, user_id: UUID):
        return self.repo.get_by_id(user_id)

    def get_user_by_id_and_tenant(self, user_id: UUID, tenant_id: UUID):
        return self.repo.get_by_id_and_tenant(user_id, tenant_id)

    def get_user_by_username_and_tenant(self, username: str, tenant_id: UUID):
        return self.repo.get_by_username_and_tenant(username, tenant_id)

    def get_user_by_email_and_tenant(self, email: str, tenant_id: UUID):
        return self.repo.get_by_email_and_tenant(email, tenant_id)

    def get_users_by_tenant(self, tenant_id: UUID, skip: int = 0, limit: int = 100):
        return self.repo.get_all_by_tenant(tenant_id, skip, limit)

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
        tenant,
        name: Optional[str] = None,
        surname: Optional[str] = None,
        role: str = "client",
    ):
        # Check if username/email exists within this tenant
        existing_user = self.repo.get_by_username_or_email_and_tenant(
            username, email, tenant.id
        )
        if existing_user:
            raise HTTPException(
                status_code=400, detail="error.username_or_email_already_in_use"
            )

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode(
            "utf-8"
        )
        new_user = User(
            username=username,
            email=email,
            hashed_password=hashed,
            tenant_id=tenant.id,
            name=name,
            surname=surname,
            role=role,
        )
        return self.repo.create(new_user)
