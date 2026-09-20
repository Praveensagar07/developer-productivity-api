"""Automated tests for Task management endpoints and status workflows."""

from fastapi.testclient import TestClient


def _setup_project_and_user(client: TestClient) -> tuple[dict, dict]:
    """Helper fixture to create user and project for task testing."""
    user = client.post(
        "/api/v1/users",
        json={"name": "Dev Lead", "email": "lead@example.com"},
    ).json()["data"]

    project = client.post(
        "/api/v1/projects",
        json={"name": "Backend Services", "owner_id": user["id"]},
    ).json()["data"]

    return user, project


def test_create_task_success(client: TestClient) -> None:
    """Verify creating a valid task with project and assignee references."""
    user, project = _setup_project_and_user(client)

    payload = {
        "title": "Build centralized error handlers",
        "description": "Standardize JSON responses for all domain errors.",
        "project_id": project["id"],
        "assignee_id": user["id"],
        "status": "todo",
        "priority": "high",
    }
    response = client.post("/api/v1/tasks", json=payload)
    assert response.status_code == 201
    task = response.json()["data"]
    assert task["title"] == payload["title"]
    assert task["project_id"] == project["id"]
    assert task["assignee_id"] == user["id"]
    assert task["status"] == "todo"
    assert task["priority"] == "high"
    assert task["id"].startswith("tsk_")


def test_create_task_invalid_project(client: TestClient) -> None:
    """Verify creating task with non-existent project returns 404."""
    user = client.post(
        "/api/v1/users",
        json={"name": "User", "email": "usr@example.com"},
    ).json()["data"]

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Floating Task",
            "project_id": "prj_nonexistent_999",
            "assignee_id": user["id"],
        },
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "RESOURCE_NOT_FOUND"


def test_create_task_invalid_assignee(client: TestClient) -> None:
    """Verify creating task with non-existent assignee returns 404."""
    user, project = _setup_project_and_user(client)

    response = client.post(
        "/api/v1/tasks",
        json={
            "title": "Invalid Assignee Task",
            "project_id": project["id"],
            "assignee_id": "usr_invalid_ghost_999",
        },
    )
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "RESOURCE_NOT_FOUND"


def test_get_task_success(client: TestClient) -> None:
    """Verify retrieving existing task."""
    user, project = _setup_project_and_user(client)
    task = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "project_id": project["id"]},
    ).json()["data"]

    res = client.get(f"/api/v1/tasks/{task['id']}")
    assert res.status_code == 200
    assert res.json()["data"]["title"] == "Test Task"


def test_get_task_not_found(client: TestClient) -> None:
    """Verify retrieving non-existent task returns 404."""
    res = client.get("/api/v1/tasks/tsk_missing_999")
    assert res.status_code == 404
    assert res.json()["error"]["code"] == "RESOURCE_NOT_FOUND"


def test_update_task(client: TestClient) -> None:
    """Verify general task updates."""
    user, project = _setup_project_and_user(client)
    task = client.post(
        "/api/v1/tasks",
        json={"title": "Old Title", "project_id": project["id"]},
    ).json()["data"]

    res = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={
            "title": "New Title",
            "description": "Updated description",
            "priority": "critical",
        },
    )
    assert res.status_code == 200
    updated = res.json()["data"]
    assert updated["title"] == "New Title"
    assert updated["priority"] == "critical"


def test_update_task_status_dedicated_endpoint(client: TestClient) -> None:
    """Verify dedicated PATCH /api/v1/tasks/{id}/status endpoint transitions."""
    user, project = _setup_project_and_user(client)
    task = client.post(
        "/api/v1/tasks",
        json={
            "title": "Status Workflow Test",
            "project_id": project["id"],
            "status": "todo",
        },
    ).json()["data"]
    assert task["status"] == "todo"

    # Move to in-progress
    res1 = client.patch(
        f"/api/v1/tasks/{task['id']}/status",
        json={"status": "in-progress"},
    )
    assert res1.status_code == 200
    assert res1.json()["data"]["status"] == "in-progress"

    # Move to done
    res2 = client.patch(
        f"/api/v1/tasks/{task['id']}/status",
        json={"status": "done"},
    )
    assert res2.status_code == 200
    assert res2.json()["data"]["status"] == "done"


def test_update_task_status_invalid_value(client: TestClient) -> None:
    """Verify invalid status string returns 422 validation error."""
    user, project = _setup_project_and_user(client)
    task = client.post(
        "/api/v1/tasks",
        json={"title": "Test Task", "project_id": project["id"]},
    ).json()["data"]

    res = client.patch(
        f"/api/v1/tasks/{task['id']}/status",
        json={"status": "completed"},  # 'completed' is invalid for task, valid are: todo, in-progress, done
    )
    assert res.status_code == 422
    assert res.json()["error"]["code"] == "VALIDATION_ERROR"


def test_delete_task(client: TestClient) -> None:
    """Verify task deletion."""
    user, project = _setup_project_and_user(client)
    task = client.post(
        "/api/v1/tasks",
        json={"title": "Task to Delete", "project_id": project["id"]},
    ).json()["data"]

    del_res = client.delete(f"/api/v1/tasks/{task['id']}")
    assert del_res.status_code == 200
    assert del_res.json()["data"]["id"] == task["id"]

    get_res = client.get(f"/api/v1/tasks/{task['id']}")
    assert get_res.status_code == 404
