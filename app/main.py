"""Main FastAPI application entrypoint."""

import sys
import time
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncGenerator

# Ensure project root is in sys.path when executed directly or in serverless runtimes
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import get_settings
from app.core.error_handlers import register_error_handlers
from app.data.seed import seed_data
from app.data.store import get_store

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager handling startup and teardown routines."""
    # Startup: seed in-memory store with development dataset if enabled
    if settings.seed_data_on_startup:
        seed_data(get_store())
    yield
    # Teardown logic if needed in future weeks


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
# Developer Productivity REST API

Welcome to the **Users, Projects & Tasks REST API** built for **Week 2 — Task 2** of the **Innovation Hacks Full Stack Development Internship**.

### Internship Roadmap
- **Week 1 (Task 1):** Frontend Developer Productivity Dashboard (React/Tailwind)
- **Week 2 (Task 2 - Current):** RESTful Backend API (Python / FastAPI / In-Memory Repository)
- **Week 3 (Task 3):** Database Persistence & Migrations
- **Week 4 (Task 4):** Final Full-Stack AI Productivity Platform

### Key Capabilities
- **User Management:** Full CRUD with email uniqueness and role assignment.
- **Project Management:** Project tracking with owner validation and lifecycle state management.
- **Task Management:** Work item assignment, project relationships, priority levels, and dedicated status workflow (`todo`, `in-progress`, `done`).
- **Standardized Formats:** Consistent `{ "data": ... }` envelopes, paginated collections, and structured error payloads.
- **Centralized Error Handling:** Uniform error responses across domain exceptions and input validation.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

# ----------------------------------------------------
# 1. Centralized Error Handlers
# ----------------------------------------------------
register_error_handlers(app)

# ----------------------------------------------------
# 2. CORS Middleware
# ----------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
)


# ----------------------------------------------------
# 3. Observability Middlewares (Request ID & Latency)
# ----------------------------------------------------
@app.middleware("http")
async def add_observability_headers(request: Request, call_next) -> Response:
    """Inject correlation ID and response execution time headers."""
    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time_ms:.2f}ms"
    return response


# ----------------------------------------------------
# 4. Root & Health Endpoints
# ----------------------------------------------------
@app.get(
    "/",
    tags=["System"],
    summary="API Root Information",
    description="Provides basic metadata, version info, and navigation links.",
)
def root_info() -> dict[str, str]:
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.app_env,
        "docs": "/docs",
        "redoc": "/redoc",
        "api_v1": settings.api_prefix,
    }


@app.get(
    "/health",
    tags=["System"],
    summary="Health Status Check",
    description="Returns service health status, UTC timestamp, and version indicator.",
)
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.app_version,
        "environment": settings.app_env,
    }


# ----------------------------------------------------
# 5. Versioned API Router Inclusion
# ----------------------------------------------------
app.include_router(api_router, prefix=settings.api_prefix)
