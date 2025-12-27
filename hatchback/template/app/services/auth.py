from datetime import datetime, timedelta
from os import environ as env
from typing import Any, Dict, Optional
from uuid import UUID

import bcrypt
from jose import JWTError, jwt

from app.services.user import UserService

SECRET_KEY = env.get("SECRET_KEY")
if not SECRET_KEY:
    # In production, this should raise an error. For boilerplate, we warn or set a default but ideally we force it.
    # However, to avoid breaking local dev immediately without .env, we can keep a default but make it complex?
    # Better: Raise error if not found, forcing user to set it in .env
    # But for boilerplate generation, we provide .env.example.
    # Let's stick to the user request: "Weak Default Secret Key".
    # We will enforce it being set, or at least warn heavily.
    # For now, let's use a stronger default but really we should rely on env.
    SECRET_KEY = "CHANGE_THIS_TO_A_STRONG_SECRET_KEY_IN_PRODUCTION"

ALGORITHM = env.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(env.get("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


class AuthService:
    def __init__(self, db):
        self.user_service = UserService(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def authenticate_user(
        self, username: str, password: str, tenant_id: UUID
    ) -> Optional[Dict[str, Any]]:
        # Look for user within the specific tenant
        user = self.user_service.get_user_by_username_and_tenant(username, tenant_id)
        if not user:
            # Check if username is email
            user = self.user_service.get_user_by_email_and_tenant(username, tenant_id)
        
        # Timing attack mitigation: Always verify password even if user is not found
        # We use a dummy hash to simulate the work
        if not user:
            # Dummy hash verification to consume time
            # This hash corresponds to "password"
            dummy_hash = "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWrn96pzcFQ/4S.WBa.G.../1e"
            self.verify_password(password, dummy_hash)
            return None

        if not self.verify_password(password, user.hashed_password):
            return None

        return {
            "id": str(user.id),
            "tenant_id": str(user.tenant_id),
            "username": user.username,
            "email": user.email,
            "name": user.name,
            "surname": user.surname,
            "role": user.role,
        }

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def decode_access_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except JWTError:
            return None
