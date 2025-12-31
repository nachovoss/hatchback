import pytest
from unittest.mock import MagicMock
from app.services.auth import AuthService
from app.services.notification import NotificationService
from app.models.user import User
from uuid import uuid4

def test_forgot_password_sends_email(db_session):
    # Mock dependencies
    auth_service = AuthService(db_session)
    auth_service.user_service = MagicMock()
    auth_service.notification_service = MagicMock()
    
    # Setup mock user
    user = User(id=uuid4(), email="test@example.com", tenant_id=uuid4())
    auth_service.user_service.get_user_by_email_and_tenant.return_value = user
    
    # Call method
    auth_service.forgot_password("test@example.com", user.tenant_id)
    
    # Verify email sent
    auth_service.notification_service.send_password_recovery_email.assert_called_once()
    args = auth_service.notification_service.send_password_recovery_email.call_args
    assert args[0][0] == "test@example.com"
    assert args[0][1] is not None # Token

def test_forgot_password_user_not_found(db_session):
    # Mock dependencies
    auth_service = AuthService(db_session)
    auth_service.user_service = MagicMock()
    auth_service.notification_service = MagicMock()
    
    # Setup mock user not found
    auth_service.user_service.get_user_by_email_and_tenant.return_value = None
    
    # Call method
    auth_service.forgot_password("test@example.com", uuid4())
    
    # Verify email NOT sent
    auth_service.notification_service.send_password_recovery_email.assert_not_called()

def test_reset_password_success(db_session):
    # Mock dependencies
    auth_service = AuthService(db_session)
    auth_service.user_service = MagicMock()
    
    # Create valid token
    user_id = uuid4()
    token = auth_service.create_access_token(
        data={"sub": str(user_id), "type": "reset_password"}
    )
    
    # Setup mock user
    user = User(id=user_id)
    auth_service.user_service.get_user_by_id.return_value = user
    
    # Call method
    auth_service.reset_password(token, "newpassword")
    
    # Verify update called
    auth_service.user_service.update_user.assert_called_once()
    assert auth_service.user_service.update_user.call_args[0][0] == user
    assert auth_service.user_service.update_user.call_args[0][1] == {"password": "newpassword"}
