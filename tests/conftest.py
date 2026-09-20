"""Pytest fixtures and test environment configuration."""

from typing import Generator
import pytest
from fastapi.testclient import TestClient
from app.data.seed import seed_data
from app.data.store import get_store, reset_store
from app.main import app


@pytest.fixture(autouse=True)
def reset_in_memory_store() -> Generator[None, None, None]:
    """Ensure in-memory storage is wiped clean before and after each test."""
    reset_store()
    yield
    reset_store()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide a test client against an empty database."""
    with TestClient(app) as test_client:
        reset_store()
        yield test_client
        reset_store()


@pytest.fixture
def seeded_client() -> Generator[TestClient, None, None]:
    """Provide a test client against pre-seeded realistic development data."""
    with TestClient(app) as test_client:
        reset_store()
        seed_data(get_store())
        yield test_client
        reset_store()
