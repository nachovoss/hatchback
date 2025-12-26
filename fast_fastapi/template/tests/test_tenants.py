def test_read_main(client):
    """
    Test that the app is running (health check or similar).
    Since we don't have a root endpoint, we check 404 or docs.
    """
    response = client.get("/docs")
    assert response.status_code == 200

def test_create_tenant(client):
    """
    Test creating a new tenant.
    """
    response = client.post(
        "/tenants",
        json={"name": "Test Tenant", "subdomain": "test_subdomain", "domain": "test.com"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Tenant"
    assert "id" in data

def test_read_tenants(client):
    """
    Test reading tenants.
    """
    # Create a tenant first
    client.post(
        "/tenants",
        json={"name": "Tenant 1", "subdomain": "subdomain1", "domain": "t1.com"}
    )
    client.post(
        "/tenants",
        json={"name": "Tenant 2", "subdomain": "subdomain2", "domain": "t2.com"}
    )

    response = client.get("/tenants")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
