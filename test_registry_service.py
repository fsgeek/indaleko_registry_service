# test_registry_service.py

"""
Basic tests for the Registry Service API.
Designed for a separate intern to use as their starting point.
Covers: registration, resolution, property updates, and error handling.
"""

from uuid import UUID

import httpx
import pytest

BASE_URL = "http://localhost:8000"

@pytest.fixture(scope="session")
def client():
    with httpx.Client(base_url=BASE_URL) as c:
        yield c

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
