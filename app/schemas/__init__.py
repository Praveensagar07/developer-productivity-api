"""Pydantic schemas and serialization models."""

from app.schemas.common import (
    BaseSchema,
    DataResponse,
    ErrorBody,
    ErrorDetail,
    ErrorResponse,
    MessageData,
    MessageResponse,
    PaginatedResponse,
    PaginationMeta,
)
from app.schemas.project import (
    ProjectCreate,
    ProjectPriority,
    ProjectResponse,
    ProjectStatus,
    ProjectUpdate,
)
from app.schemas.task import (
    TaskCreate,
    TaskPriority,
    TaskResponse,
    TaskStatus,
    TaskStatusUpdate,
    TaskUpdate,
)
from app.schemas.user import UserCreate, UserResponse, UserRole, UserUpdate

__all__ = [
    "BaseSchema",
    "DataResponse",
    "ErrorBody",
    "ErrorDetail",
    "ErrorResponse",
    "MessageData",
    "MessageResponse",
    "PaginatedResponse",
    "PaginationMeta",
    "UserRole",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "ProjectStatus",
    "ProjectPriority",
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
    "TaskStatus",
    "TaskPriority",
    "TaskCreate",
    "TaskUpdate",
    "TaskStatusUpdate",
    "TaskResponse",
]
