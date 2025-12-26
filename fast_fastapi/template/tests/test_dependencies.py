import pytest
from fastapi import HTTPException
from app.dependencies import get_current_active_user, RoleChecker
from app.models.user import User

def test_get_current_active_user_active():
    """
    Test that an active user is returned successfully.
    """
    user = User(username="test", email="test@test.com", status="active")
    result = get_current_active_user(user)
    assert result == user

def test_get_current_active_user_inactive():
    """
    Test that an inactive user raises an HTTPException.
    """
    user = User(username="test", email="test@test.com", status="suspended")
    with pytest.raises(HTTPException) as excinfo:
        get_current_active_user(user)
    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "error.inactive_user"

def test_role_checker_allowed():
    """
    Test that a user with an allowed role is permitted.
    """
    user = User(username="test", email="test@test.com", status="active", role="admin")
    checker = RoleChecker(["admin", "superadmin"])
    # We pass the user directly, bypassing the dependency injection for unit testing
    result = checker(user)
    assert result == user

def test_role_checker_forbidden():
    """
    Test that a user without an allowed role raises an HTTPException.
    """
    user = User(username="test", email="test@test.com", status="active", role="client")
    checker = RoleChecker(["admin"])
    with pytest.raises(HTTPException) as excinfo:
        checker(user)
    assert excinfo.value.status_code == 403
    assert excinfo.value.detail == "error.operation_not_permitted"
