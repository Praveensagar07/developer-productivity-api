"""Automated tests for Project management endpoints."""

from fastapi.testclient import TestClient


def test_create_project_success(client: TestClient) -> None:
    """Verify creating a project with a valid owner returns 201 Created."""
    user = client.post(
        "/api/v1/users",
        json={"name": "Project Owner", "email": "owner@example.com"},
    ).json()["data"]

    payload = {
        "name": "Cloud Migration",
        "description": "Migrate core microservices to Kubernetes clusters.",
        "status": "planning",
        "priority": "high",
        "owner_id": user["id"],
    }
    response = client.post("/api/v1/projects", json=payload)
    assert response.status_code == 201
    proj = response.json()["data"]
    assert proj["name"] == "Cloud Migration"
    assert proj["owner_id"] == user["id"]
    assert proj["status"] == "planning"
    assert proj["priority"] == "high"
    assert proj["id"].startswith("prj_")


def test_create_project_invalid_owner(client: TestClient) -> None:
    """Verify creating project with non-existent owner returns 404 Not Found."""
    payload = {
        "name": "Ghost Project",
        "owner_id": "usr_does_not_exist_999",
    }
    response = client.post("/api/v1/projects", json=payload)
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "RESOURCE_NOT_FOUND"
    assert "does not exist" in error["message"]


def test_create_project_invalid_input(client: TestClient) -> None:
    """Verify invalid status or missing name returns 422."""
    user = client.post(
        "/api/v1/users",
        json={"name": "Project Owner", "email": "owner@example.com"},
    ).json()["data"]

    # Invalid status enum
    res = client.post(
        "/api/v1/projects",
        json={
            "name": "Valid Name",
            "owner_id": user["id"],
            "status": "invalid_status",
        },
    )
    assert res.status_code == 422

    # Blank name
    res2 = client.post(
        "/api/v1/projects",
        json={
            "name": "   ",
            "owner_id": user["id"],
        },
    )
    assert res2.status_code == 422


def test_get_project_success(client: TestClient) -> None:
    """Verify retrieving project by ID."""
    user = client.post(
        "/api/v1/users",
        json={"name": "Owner", "email": "owner2@example.com"},
    ).json()["data"]
    proj = client.post(
        "/api/v1/projects",
        json={"name": "Analytics Dashboard", "owner_id": user["id"]},
    ).json()["data"]

    res = client.get(f"/api/v1/projects/{proj['id']}")
    assert res.status_code == 200
    assert res.json()["data"]["name"] == "Analytics Dashboard"


def test_get_project_not_found(client: TestClient) -> None:
    """Verify non-existent project lookup yields 404."""
    res = client.get("/api/v1/projects/prj_unknown_404")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "RESOURCE_NOT_FOUND"


def test_update_project(client: TestClient) -> None:
    """Verify updating project fields."""
    u1 = client.post(
        "/api/v1/users",
        json={"name": "Owner 1", "email": "owner1@example.com"},
    ).json()["data"]
    u2 = client.post(
        "/api/v1/users",
        json={"name": "Owner 2", "email": "owner2@example.com"},
    ).json()["data"]

    proj = client.post(
        "/api/v1/projects",
        json={"name": "Initial Name", "owner_id": u1["id"]},
    ).json()["data"]

    res = client.patch(
        f"/api/v1/projects/{proj['id']}",
        json={
            "name": "Updated Name",
            "status": "active",
            "priority": "critical",
            "owner_id": u2["id"],
        },
    )
    assert res.status_code == 200
    updated = res.json()["data"]
    assert updated["name"] == "Updated Name"
    assert updated["status"] == "active"
    assert updated["priority"] == "critical"
    assert updated["owner_id"] == u2["id"]


def test_delete_project(client: TestClient) -> None:
    """Verify deleting project succeeds."""
    user = client.post(
        "/api/v1/users",
        json={"name": "Owner", "email": "del_owner@example.com"},
    ).json()["data"]
    proj = client.post(
        "/api/v1/projects",
        json={"name": "To Delete", "owner_id": user["id"]},
    ).json()["data"]

    res = client.delete(f"/api/v1/projects/{proj['id']}")
    assert res.status_code == 200
    assert res.json()["data"]["id"] == proj["id"]

    get_res = client.get(f"/api/v1/projects/{proj['id']}")
    assert get_res.status_code == 404
