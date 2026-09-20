"""Thread-safe in-memory data store for Week 2 development."""

import threading
from app.models.user import User
from app.models.project import Project
from app.models.task import Task


class InMemoryStore:
    """Thread-safe centralized memory store for domain entities."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.users: dict[str, User] = {}
        self.projects: dict[str, Project] = {}
        self.tasks: dict[str, Task] = {}

    def clear(self) -> None:
        """Clear all stored data (useful for test isolation)."""
        with self._lock:
            self.users.clear()
            self.projects.clear()
            self.tasks.clear()

    @property
    def lock(self) -> threading.RLock:
        """Expose lock for transactional atomicity."""
        return self._lock


# Global application store singleton
_global_store = InMemoryStore()


def get_store() -> InMemoryStore:
    """FastAPI dependency provider for the centralized in-memory store."""
    return _global_store


def reset_store() -> None:
    """Reset global store to blank state."""
    _global_store.clear()
