"""API route handlers."""

from app.api.routes.projects import router as projects_router
from app.api.routes.tasks import router as tasks_router
from app.api.routes.users import router as users_router

__all__ = ["users_router", "projects_router", "tasks_router"]
