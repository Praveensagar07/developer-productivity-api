"""Automated tests for centralized error formats, health, and system middleware."""

from fastapi.testclient import TestClient


def test_health_endpoint(client: TestClient) -> None:
    """Verify GET /health returns 200 OK and expected structure."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "timestamp" in data
    assert "environment" in data


def test_root_endpoint(client: TestClient) -> None:
    """Verify GET / returns API metadata and doc paths."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "version" in data
    assert data["docs"] == "/docs"
    assert data["api_v1"] == "/api/v1"


def test_observability_headers(client: TestClient) -> None:
    """Verify response contains X-Request-ID and X-Process-Time headers."""
    response = client.get("/health")
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers
    assert response.headers["X-Process-Time"].endswith("ms")

    custom_req_id = "test-custom-request-id-12345"
    res_with_id = client.get("/health", headers={"X-Request-ID": custom_req_id})
    assert res_with_id.headers["X-Request-ID"] == custom_req_id


def test_centralized_error_envelope_structure(client: TestClient) -> None:
    """Verify error envelope adheres strictly to the required specification."""
    # 404 test
    res_404 = client.get("/api/v1/users/usr_nonexistent")
    assert res_404.status_code == 404
    body_404 = res_404.json()
    assert "error" in body_404
    assert body_404["error"]["code"] == "RESOURCE_NOT_FOUND"
    assert isinstance(body_404["error"]["message"], str)
    assert isinstance(body_404["error"]["details"], list)

    # 422 test
    res_422 = client.post("/api/v1/users", json={"name": ""})
    assert res_422.status_code == 422
    body_422 = res_422.json()
    assert "error" in body_422
    assert body_422["error"]["code"] == "VALIDATION_ERROR"
    assert len(body_422["error"]["details"]) > 0

    # Check that stack traces or sensitive internal paths are not exposed
    assert "Traceback" not in res_422.text
    assert "Traceback" not in res_404.text
