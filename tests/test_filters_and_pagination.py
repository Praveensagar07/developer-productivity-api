"""Automated tests for filtering parameters and pagination logic."""

from fastapi.testclient import TestClient


def test_task_filtering_by_status(seeded_client: TestClient) -> None:
    """Verify filtering tasks by status."""
    res_todo = seeded_client.get("/api/v1/tasks?status=todo")
    assert res_todo.status_code == 200
    data_todo = res_todo.json()["data"]
    assert len(data_todo) > 0
    assert all(t["status"] == "todo" for t in data_todo)

    res_in_prog = seeded_client.get("/api/v1/tasks?status=in-progress")
    assert res_in_prog.status_code == 200
    data_in_prog = res_in_prog.json()["data"]
    assert len(data_in_prog) > 0
    assert all(t["status"] == "in-progress" for t in data_in_prog)

    res_done = seeded_client.get("/api/v1/tasks?status=done")
    assert res_done.status_code == 200
    data_done = res_done.json()["data"]
    assert len(data_done) > 0
    assert all(t["status"] == "done" for t in data_done)


def test_task_filtering_by_priority(seeded_client: TestClient) -> None:
    """Verify filtering tasks by priority."""
    res = seeded_client.get("/api/v1/tasks?priority=critical")
    assert res.status_code == 200
    items = res.json()["data"]
    assert len(items) > 0
    assert all(t["priority"] == "critical" for t in items)


def test_task_filtering_by_project_and_assignee(seeded_client: TestClient) -> None:
    """Verify filtering tasks by project_id and assignee_id."""
    res = seeded_client.get("/api/v1/tasks?project_id=prj_dev_dashboard")
    assert res.status_code == 200
    items = res.json()["data"]
    assert len(items) > 0
    assert all(t["project_id"] == "prj_dev_dashboard" for t in items)

    res_assignee = seeded_client.get("/api/v1/tasks?assignee_id=usr_taylor_chen")
    assert res_assignee.status_code == 200
    items_assignee = res_assignee.json()["data"]
    assert len(items_assignee) > 0
    assert all(t["assignee_id"] == "usr_taylor_chen" for t in items_assignee)


def test_task_combined_filtering(seeded_client: TestClient) -> None:
    """Verify combined filtering on project, status, and priority."""
    res = seeded_client.get(
        "/api/v1/tasks?project_id=prj_dev_dashboard&status=done&priority=high"
    )
    assert res.status_code == 200
    items = res.json()["data"]
    assert len(items) > 0
    for t in items:
        assert t["project_id"] == "prj_dev_dashboard"
        assert t["status"] == "done"
        assert t["priority"] == "high"


def test_pagination_bounds_and_validation(client: TestClient) -> None:
    """Verify pagination validation on skip and limit parameters."""
    # Negative skip should be rejected with 422
    res_neg_skip = client.get("/api/v1/users?skip=-1")
    assert res_neg_skip.status_code == 422
    assert res_neg_skip.json()["error"]["code"] == "VALIDATION_ERROR"

    # Zero limit should be rejected with 422 (limit must be >= 1)
    res_zero_limit = client.get("/api/v1/users?limit=0")
    assert res_zero_limit.status_code == 422

    # Limit > 100 should be rejected with 422 (limit must be <= 100)
    res_huge_limit = client.get("/api/v1/users?limit=150")
    assert res_huge_limit.status_code == 422


def test_project_filtering_by_status(seeded_client: TestClient) -> None:
    """Verify project filtering by status."""
    res = seeded_client.get("/api/v1/projects?status=active")
    assert res.status_code == 200
    items = res.json()["data"]
    assert len(items) > 0
    assert all(p["status"] == "active" for p in items)
