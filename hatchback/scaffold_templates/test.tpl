import pytest
from app.models.__resource__ import __Resource__

def test_create___resource__(client, db_session):
    # TODO: Update payload with required fields for __Resource__
    payload = {
        # "name": "Test __Resource__",
        # "description": "Test Description"
    }
    
    # response = client.post("/__resource__s/", json=payload)
    # assert response.status_code == 200
    # data = response.json()
    # assert "id" in data

def test_read___resource__s(client, db_session):
    response = client.get("/__resource__s/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read___resource___by_id(client, db_session):
    # TODO: Create a __Resource__ in the database first
    # item = __Resource__(...)
    # db_session.add(item)
    # db_session.commit()
    
    # response = client.get(f"/__resource__s/{item.id}")
    # assert response.status_code == 200
    # assert response.json()["id"] == str(item.id)
    pass

def test_update___resource__(client, db_session):
    # TODO: Create a __Resource__ in the database first
    # item = __Resource__(...)
    # db_session.add(item)
    # db_session.commit()

    update_payload = {
        # "name": "Updated Name"
    }

    # response = client.put(f"/__resource__s/{item.id}", json=update_payload)
    # assert response.status_code == 200
    # assert response.json()["name"] == "Updated Name"
    pass

def test_delete___resource__(client, db_session):
    # TODO: Create a __Resource__ in the database first
    # item = __Resource__(...)
    # db_session.add(item)
    # db_session.commit()

    # response = client.delete(f"/__resource__s/{item.id}")
    # assert response.status_code == 200
    
    # Verify it's gone
    # response = client.get(f"/__resource__s/{item.id}")
    # assert response.status_code == 404
    pass
