"""User domain entity."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return current timezone-aware UTC datetime."""
    return datetime.now(timezone.utc)


@dataclass
class User:
    """User domain entity representing a team member or system user."""

    id: str
    name: str
    email: str
    role: str = "developer"
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
