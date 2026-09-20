"""User in-memory repository implementation."""

from app.data.store import InMemoryStore, get_store
from app.models.user import User
from fastapi import Depends


class UserRepository:
    """In-memory data access layer for User entities."""

    def __init__(self, store: InMemoryStore = Depends(get_store)) -> None:
        self.store = store

    def get_by_id(self, user_id: str) -> User | None:
        """Find user by ID."""
        with self.store.lock:
            return self.store.users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        """Find user by case-insensitive email."""
        target = email.strip().lower()
        with self.store.lock:
            for user in self.store.users.values():
                if user.email.lower() == target:
                    return user
            return None

    def list_users(
        self,
        skip: int = 0,
        limit: int = 20,
        role: str | None = None,
    ) -> tuple[list[User], int]:
        """List users with optional role filter and pagination."""
        with self.store.lock:
            items = list(self.store.users.values())
            if role:
                target_role = role.strip().lower()
                items = [u for u in items if u.role.lower() == target_role]

            total = len(items)
            paginated = items[skip : skip + limit]
            return paginated, total

    def create(self, user: User) -> User:
        """Persist a new user."""
        with self.store.lock:
            self.store.users[user.id] = user
            return user

    def update(self, user: User) -> User:
        """Persist an updated user."""
        with self.store.lock:
            self.store.users[user.id] = user
            return user

    def delete(self, user_id: str) -> bool:
        """Remove user by ID."""
        with self.store.lock:
            if user_id in self.store.users:
                del self.store.users[user_id]
                return True
            return False

    def count(self) -> int:
        """Total user count."""
        with self.store.lock:
            return len(self.store.users)
