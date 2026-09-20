"""End-to-end integration test validating the complete 13-step workflow."""

from fastapi.testclient import TestClient


def test_complete_thirteen_step_demo_workflow(client: TestClient) -> None:
    """Execute the end-to-end demo workflow covering the entire domain model lifecycle:
    1. Create user A
    2. Create user B
    3. Create project owned by user A
    4. Create task under that project
    5. Assign task to user B
    6. Retrieve the task
    7. Change status from todo to in-progress
    8. Change status to done
    9. Filter tasks
    10. Update the task
    11. Delete the task
    12. Retrieve the project
    13. Retrieve the users
    """
    # 1. Create a user (User A)
    res1 = client.post(
        "/api/v1/users",
        json={
            "name": "Alice Architect",
            "email": "alice.arch@example.com",
            "role": "lead_architect",
        },
    )
    assert res1.status_code == 201
    user_a = res1.json()["data"]
    assert user_a["email"] == "alice.arch@example.com"

    # 2. Create another user (User B)
    res2 = client.post(
        "/api/v1/users",
        json={
            "name": "Bob Builder",
            "email": "bob.builder@example.com",
            "role": "developer",
        },
    )
    assert res2.status_code == 201
    user_b = res2.json()["data"]
    assert user_b["email"] == "bob.builder@example.com"

    # 3. Create a project owned by user A
    res3 = client.post(
        "/api/v1/projects",
        json={
            "name": "Distributed Event Engine",
            "description": "High throughput event processing platform.",
            "status": "active",
            "priority": "critical",
            "owner_id": user_a["id"],
        },
    )
    assert res3.status_code == 201
    project = res3.json()["data"]
    assert project["owner_id"] == user_a["id"]

    # 4 & 5. Create a task under that project and assign it to user B
    res4 = client.post(
        "/api/v1/tasks",
        json={
            "title": "Implement Kafka consumer group",
            "description": "Ensure exactly-once processing semantics.",
            "project_id": project["id"],
            "assignee_id": user_b["id"],
            "status": "todo",
            "priority": "high",
        },
    )
    assert res4.status_code == 201
    task = res4.json()["data"]
    assert task["project_id"] == project["id"]
    assert task["assignee_id"] == user_b["id"]
    assert task["status"] == "todo"

    # 6. Retrieve the task
    res6 = client.get(f"/api/v1/tasks/{task['id']}")
    assert res6.status_code == 200
    assert res6.json()["data"]["id"] == task["id"]

    # 7. Change status from todo to in-progress
    res7 = client.patch(
        f"/api/v1/tasks/{task['id']}/status",
        json={"status": "in-progress"},
    )
    assert res7.status_code == 200
    assert res7.json()["data"]["status"] == "in-progress"

    # 8. Change status to done
    res8 = client.patch(
        f"/api/v1/tasks/{task['id']}/status",
        json={"status": "done"},
    )
    assert res8.status_code == 200
    assert res8.json()["data"]["status"] == "done"

    # 9. Filter tasks
    res9 = client.get(f"/api/v1/tasks?project_id={project['id']}&status=done")
    assert res9.status_code == 200
    matching_tasks = res9.json()["data"]
    assert len(matching_tasks) == 1
    assert matching_tasks[0]["id"] == task["id"]

    # 10. Update the task (e.g. description or priority)
    res10 = client.patch(
        f"/api/v1/tasks/{task['id']}",
        json={
            "title": "Implement Kafka consumer group v2",
            "priority": "critical",
        },
    )
    assert res10.status_code == 200
    updated_task = res10.json()["data"]
    assert updated_task["title"] == "Implement Kafka consumer group v2"
    assert updated_task["priority"] == "critical"

    # 11. Delete the task
    res11 = client.delete(f"/api/v1/tasks/{task['id']}")
    assert res11.status_code == 200
    assert res11.json()["data"]["id"] == task["id"]

    # Confirm deletion returns 404
    res11_verify = client.get(f"/api/v1/tasks/{task['id']}")
    assert res11_verify.status_code == 404

    # 12. Retrieve the project
    res12 = client.get(f"/api/v1/projects/{project['id']}")
    assert res12.status_code == 200
    assert res12.json()["data"]["id"] == project["id"]

    # 13. Retrieve the users
    res13_a = client.get(f"/api/v1/users/{user_a['id']}")
    assert res13_a.status_code == 200
    assert res13_a.json()["data"]["name"] == "Alice Architect"

    res13_b = client.get(f"/api/v1/users/{user_b['id']}")
    assert res13_b.status_code == 200
    assert res13_b.json()["data"]["name"] == "Bob Builder"
