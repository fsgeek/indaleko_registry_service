# test_registry_service.py

"""
Basic tests for the Registry Service API.
Designed for a separate intern to use as their starting point.
Covers: registration, resolution, property updates, and error handling.
"""

from uuid import UUID

import httpx
import pytest

BASE_URL = "http://testserver"

@pytest.fixture(scope="session")
def client(tmp_path_factory):
    # Override the SQLite DB path for isolation
    import registry_service.service as service
    from fastapi.testclient import TestClient

    # Prepare temporary SQLite file
    db_file = tmp_path_factory.mktemp("data") / "test_registry.sqlite"
    service.db_path = str(db_file)

    # Create TestClient for in-process testing
    from registry_service.service import app
    with TestClient(app) as client:
        yield client

def test_register_and_resolve(client):
    data = {
        "category": "semantic_label",
        "name": "test_label",
        "description": "A test label for validation"
    }
    r = client.post("/register", json=data)
    assert r.status_code == 200
    result = r.json()
    uuid = UUID(result["uuid"])
    assert isinstance(uuid, UUID)

    # Resolve
    r2 = client.get(
        "/resolve",
        params={
            "category": "semantic_label",
            "name": "test_label"
        }
    )
    assert r2.status_code == 200
    assert r2.json()["uuid"] == str(uuid)

def test_conflict_on_duplicate_name(client):
    payload = {
        "category": "activity_provider",
        "name": "test_provider",
        "description": "duplicate entry test"
    }
    r1 = client.post("/register", json=payload)
    assert r1.status_code == 200
    r2 = client.post("/register", json=payload)
    assert r2.status_code == 409

def test_property_roundtrip(client):
    # First register
    reg = client.post("/register", json={
        "category": "analyzer",
        "name": "token_splitter",
        "description": "Token splitting analyzer"
    }).json()
    uid = reg["uuid"]

    prop = {
        "uuid": uid,
        "category": "analyzer",
        "properties": {"tokenizer": "whitespace", "ngram": 2},
        "cookie": {"note": "early-stage config"}
    }
    set_res = client.post("/properties", json=prop)
    assert set_res.status_code == 200
    out = set_res.json()
    assert out["properties"]["tokenizer"] == "whitespace"

    # Get
    r = client.get("/properties", params={"uuid": uid})
    assert r.status_code == 200
    result = r.json()
    assert result["properties"]["ngram"] == 2

def test_lookup_uuid_to_name(client):
    # Register a new entry to test reverse lookup
    payload = {"category": "semantic_label", "name": "lookup_test", "description": "desc"}
    resp = client.post("/register", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    uuid_str = data["uuid"]
    # Lookup by UUID
    lookup_resp = client.get("/lookup", params={"uuid": uuid_str})
    assert lookup_resp.status_code == 200
    lookup_data = lookup_resp.json()
    assert lookup_data["uuid"] == uuid_str
    assert lookup_data["category"] == payload["category"]
    assert lookup_data["name"] == payload["name"]
    
def test_lookup_unknown_uuid(client):
    # Lookup with a UUID that does not exist should return 404
    import uuid
    random_uuid = str(uuid.uuid4())
    r = client.get("/lookup", params={"uuid": random_uuid})
    assert r.status_code == 404
