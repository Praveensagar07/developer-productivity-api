"""Task in-memory repository implementation."""

from app.data.store import InMemoryStore, get_store
from app.models.task import Task
from fastapi import Depends


class TaskRepository:
    """In-memory data access layer for Task entities."""

    def __init__(self, store: InMemoryStore = Depends(get_store)) -> None:
        self.store = store

    def get_by_id(self, task_id: str) -> Task | None:
        """Find task by ID."""
        with self.store.lock:
            return self.store.tasks.get(task_id)

    def list_tasks(
        self,
        skip: int = 0,
        limit: int = 20,
        status: str | None = None,
        priority: str | None = None,
        project_id: str | None = None,
        assignee_id: str | None = None,
    ) -> tuple[list[Task], int]:
        """List tasks matching multiple optional filters with pagination."""
        with self.store.lock:
            items = list(self.store.tasks.values())

            if status:
                target_status = status.strip().lower()
                items = [t for t in items if t.status.lower() == target_status]
            if priority:
                target_priority = priority.strip().lower()
                items = [t for t in items if t.priority.lower() == target_priority]
            if project_id:
                items = [t for t in items if t.project_id == project_id]
            if assignee_id:
                items = [t for t in items if t.assignee_id == assignee_id]

            total = len(items)
            paginated = items[skip : skip + limit]
            return paginated, total

    def create(self, task: Task) -> Task:
        """Persist a new task."""
        with self.store.lock:
            self.store.tasks[task.id] = task
            return task

    def update(self, task: Task) -> Task:
        """Persist an updated task."""
        with self.store.lock:
            self.store.tasks[task.id] = task
            return task

    def delete(self, task_id: str) -> bool:
        """Remove task by ID."""
        with self.store.lock:
            if task_id in self.store.tasks:
                del self.store.tasks[task_id]
                return True
            return False

    def count(self) -> int:
        """Total task count."""
        with self.store.lock:
            return len(self.store.tasks)
