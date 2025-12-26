import pytest
from app.models.user import User
from app.models.tenant import Tenant
from app.dependencies import get_current_active_user

def test_get_users_admin(client, db_session):
    # Create a tenant
    tenant = Tenant(name="Test Tenant", subdomain="test-tenant")
    db_session.add(tenant)
    db_session.commit()
    db_session.refresh(tenant)

    # Create an admin user
    admin_user = User(
        email="admin@example.com",
        hashed_password="hashed_password",
        full_name="Admin User",
        role="admin",
        tenant_id=tenant.id,
        is_active=True
    )
    db_session.add(admin_user)
    
    # Create a regular user
    regular_user = User(
        email="user@example.com",
        hashed_password="hashed_password",
        full_name="Regular User",
        role="client",
        tenant_id=tenant.id,
        is_active=True
    )
    db_session.add(regular_user)
    db_session.commit()

    # Override dependency to authenticate as admin
    client.app.dependency_overrides[get_current_active_user] = lambda: admin_user

    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "admin@example.com"
    assert data[1]["email"] == "user@example.com"

    # Override dependency to authenticate as regular user
    client.app.dependency_overrides[get_current_active_user] = lambda: regular_user

    response = client.get("/users")
    assert response.status_code == 403

    # Clean up overrides
    client.app.dependency_overrides = {}
