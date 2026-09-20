"""Task domain entity."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class Task:
    """Task domain entity representing an actionable work item."""

    id: str
    title: str
    description: str | None
    project_id: str
    assignee_id: str | None
    status: str
    priority: str
    due_date: datetime | None = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
