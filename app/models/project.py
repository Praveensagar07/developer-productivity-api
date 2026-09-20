"""Project domain entity."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class Project:
    """Project domain entity representing a tracked initiative."""

    id: str
    name: str
    description: str | None
    status: str
    priority: str
    owner_id: str
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
