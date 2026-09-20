"""Automated tests for User management endpoints."""

from fastapi.testclient import TestClient


def test_create_user_success(client: TestClient) -> None:
    """Verify creating a user returns 201 Created and structured payload."""
    payload = {
        "name": "Jane Doe",
        "email": "jane.doe@example.com",
        "role": "developer",
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    json_data = response.json()
    assert "data" in json_data
    user = json_data["data"]
    assert user["name"] == "Jane Doe"
    assert user["email"] == "jane.doe@example.com"
    assert user["role"] == "developer"
    assert user["id"].startswith("usr_")
    assert "created_at" in user
    assert "updated_at" in user


def test_create_user_duplicate_email(client: TestClient) -> None:
    """Verify creating duplicate email yields 409 Conflict."""
    payload = {
        "name": "First User",
        "email": "unique@example.com",
        "role": "developer",
    }
    r1 = client.post("/api/v1/users", json=payload)
    assert r1.status_code == 201

    payload_duplicate = {
        "name": "Second User",
        "email": "unique@example.com",
        "role": "designer",
    }
    r2 = client.post("/api/v1/users", json=payload_duplicate)
    assert r2.status_code == 409
    error = r2.json()["error"]
    assert error["code"] == "DUPLICATE_RESOURCE"
    assert "already exists" in error["message"]


def test_create_user_invalid_email(client: TestClient) -> None:
    """Verify invalid email syntax produces 422 Unprocessable Entity."""
    payload = {
        "name": "Bob Smith",
        "email": "not-an-email",
        "role": "developer",
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == 422
    err = response.json()["error"]
    assert err["code"] == "VALIDATION_ERROR"
    assert len(err["details"]) > 0


def test_create_user_blank_name(client: TestClient) -> None:
    """Verify empty/blank name produces 422 validation failure."""
    payload = {
        "name": "   ",
        "email": "blank.name@example.com",
        "role": "developer",
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == 422


def test_get_user_success(client: TestClient) -> None:
    """Verify retrieving existing user by ID."""
    created = client.post(
        "/api/v1/users",
        json={"name": "Alice Wonderland", "email": "alice@example.com"},
    ).json()["data"]

    response = client.get(f"/api/v1/users/{created['id']}")
    assert response.status_code == 200
    retrieved = response.json()["data"]
    assert retrieved["id"] == created["id"]
    assert retrieved["email"] == "alice@example.com"


def test_get_user_not_found(client: TestClient) -> None:
    """Verify requesting non-existent user returns 404 Not Found."""
    response = client.get("/api/v1/users/usr_nonexistent999")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "RESOURCE_NOT_FOUND"


def test_list_users_pagination(client: TestClient) -> None:
    """Verify user listing returns paginated structure."""
    for i in range(5):
        client.post(
            "/api/v1/users",
            json={"name": f"User {i}", "email": f"user{i}@example.com"},
        )

    response = client.get("/api/v1/users?skip=1&limit=2")
    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert "meta" in body
    assert len(body["data"]) == 2
    assert body["meta"]["total"] == 5
    assert body["meta"]["skip"] == 1
    assert body["meta"]["limit"] == 2


def test_update_user(client: TestClient) -> None:
    """Verify partial user updates."""
    user = client.post(
        "/api/v1/users",
        json={"name": "Charlie Old", "email": "charlie@example.com"},
    ).json()["data"]

    patch_res = client.patch(
        f"/api/v1/users/{user['id']}",
        json={"name": "Charlie New", "role": "admin"},
    )
    assert patch_res.status_code == 200
    updated = patch_res.json()["data"]
    assert updated["name"] == "Charlie New"
    assert updated["role"] == "admin"
    assert updated["email"] == "charlie@example.com"


def test_update_user_duplicate_email_conflict(client: TestClient) -> None:
    """Verify updating to another user's email triggers 409 Conflict."""
    u1 = client.post(
        "/api/v1/users",
        json={"name": "User One", "email": "one@example.com"},
    ).json()["data"]
    u2 = client.post(
        "/api/v1/users",
        json={"name": "User Two", "email": "two@example.com"},
    ).json()["data"]

    patch_res = client.patch(
        f"/api/v1/users/{u2['id']}",
        json={"email": "one@example.com"},
    )
    assert patch_res.status_code == 409
    assert patch_res.json()["error"]["code"] == "DUPLICATE_RESOURCE"


def test_delete_user(client: TestClient) -> None:
    """Verify deleting user succeeds and subsequent retrieval returns 404."""
    user = client.post(
        "/api/v1/users",
        json={"name": "To Delete", "email": "delete.me@example.com"},
    ).json()["data"]

    del_res = client.delete(f"/api/v1/users/{user['id']}")
    assert del_res.status_code == 200
    assert del_res.json()["data"]["id"] == user["id"]

    get_res = client.get(f"/api/v1/users/{user['id']}")
    assert get_res.status_code == 404
