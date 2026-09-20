"""Project in-memory repository implementation."""

from app.data.store import InMemoryStore, get_store
from app.models.project import Project
from fastapi import Depends


class ProjectRepository:
    """In-memory data access layer for Project entities."""

    def __init__(self, store: InMemoryStore = Depends(get_store)) -> None:
        self.store = store

    def get_by_id(self, project_id: str) -> Project | None:
        """Find project by ID."""
        with self.store.lock:
            return self.store.projects.get(project_id)

    def list_projects(
        self,
        skip: int = 0,
        limit: int = 20,
        owner_id: str | None = None,
        status: str | None = None,
    ) -> tuple[list[Project], int]:
        """List projects with optional owner/status filters and pagination."""
        with self.store.lock:
            items = list(self.store.projects.values())
            if owner_id:
                items = [p for p in items if p.owner_id == owner_id]
            if status:
                target_status = status.strip().lower()
                items = [p for p in items if p.status.lower() == target_status]

            total = len(items)
            paginated = items[skip : skip + limit]
            return paginated, total

    def create(self, project: Project) -> Project:
        """Persist a new project."""
        with self.store.lock:
            self.store.projects[project.id] = project
            return project

    def update(self, project: Project) -> Project:
        """Persist an updated project."""
        with self.store.lock:
            self.store.projects[project.id] = project
            return project

    def delete(self, project_id: str) -> bool:
        """Remove project by ID."""
        with self.store.lock:
            if project_id in self.store.projects:
                del self.store.projects[project_id]
                return True
            return False

    def count(self) -> int:
        """Total project count."""
        with self.store.lock:
            return len(self.store.projects)
