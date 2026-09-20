"""Base repository interface and protocol."""

from typing import Generic, Protocol, TypeVar

T = TypeVar("T")


class BaseRepository(Protocol, Generic[T]):
    """Generic repository protocol for domain entity persistence."""

    def get_by_id(self, entity_id: str) -> T | None:
        """Fetch a single entity by its unique identifier."""
        ...

    def create(self, entity: T) -> T:
        """Store a newly created entity."""
        ...

    def update(self, entity: T) -> T:
        """Persist modifications to an existing entity."""
        ...

    def delete(self, entity_id: str) -> bool:
        """Delete an entity by ID, returning True if deleted or False if not found."""
        ...

    def count(self) -> int:
        """Return total entity count."""
        ...
