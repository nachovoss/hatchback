import pytest
from unittest.mock import MagicMock
from app.services.auth import AuthService
from app.models.user import User
from uuid import uuid4
from fastapi import HTTPException

def test_change_password_success(db_session):
    auth_service = AuthService(db_session)
    auth_service.user_service = MagicMock()
    auth_service.verify_password = MagicMock(return_value=True)
    
    user = User(id=uuid4(), hashed_password="hash")
    auth_service.user_service.get_user_by_id.return_value = user
    
    auth_service.change_password(user.id, "old_password", "new_password")
    
    auth_service.user_service.update_user.assert_called_once()
    assert auth_service.user_service.update_user.call_args[0][1] == {"password": "new_password"}

def test_change_password_wrong_current(db_session):
    auth_service = AuthService(db_session)
    auth_service.user_service = MagicMock()
    auth_service.verify_password = MagicMock(return_value=False)
    
    user = User(id=uuid4(), hashed_password="hash")
    auth_service.user_service.get_user_by_id.return_value = user
    
    with pytest.raises(HTTPException) as exc:
        auth_service.change_password(user.id, "wrong_password", "new_password")
    assert exc.value.status_code == 400
    assert exc.value.detail == "error.invalid_current_password"
