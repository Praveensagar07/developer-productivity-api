# Users, Projects & Tasks API

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-2.0+-E92063.svg?logo=pydantic)](https://docs.pydantic.dev/)
[![Tests](https://img.shields.io/badge/tests-37%20passed-success.svg)](https://pytest.org)

> **Innovation Hacks — Full Stack Development Internship**  
> **Stage:** WEEK 2 — TASK 2: Backend & REST API Development  
> **Repository:** [Praveensagar07/developer-productivity-api](https://github.com/Praveensagar07/developer-productivity-api)

---

## Overview

This repository contains the production-grade REST API developed for **Week 2 — Task 2** of the **Innovation Hacks Full Stack Development Internship**.

The backend serves as the core data and business logic engine for managing users, projects, and tasks — providing the RESTful foundation that powers the **Week 1 Developer Productivity Dashboard** and sets the architectural stage for the final full-stack platform.

### Four-Stage Internship Roadmap
```
┌───────────────────────────────┐
│   WEEK 1: Frontend Dashboard  │  Modern React/Tailwind analytics interface
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│   WEEK 2: REST API (CURRENT)  │  Layered Python/FastAPI backend & in-memory store
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│   WEEK 3: Database & ORM      │  SQL database persistence, pooling & migrations
└──────────────┬────────────────┘
               ▼
┌───────────────────────────────┐
│   WEEK 4: Full-Stack AI App   │  Integrated full-stack AI productivity platform
└───────────────────────────────┘
```
> *Note: This repository represents Week 2. Per the internship specification, persistent relational databases, migrations, and AI capabilities belong to subsequent weeks. For Week 2, a thread-safe in-memory repository pattern is utilized, engineered specifically so Week 3 can swap in a real database with minimal modifications.*

---

## Objective

Design and build a robust, modular, and self-documenting REST API that models and orchestrates users, projects, and work items with strict validation, centralized error responses, relational integrity checks, task workflow states, and OpenAPI documentation.

---

## Features

- **User Management:** Full CRUD operations with case-insensitive unique email validation, non-blank name checks, and role assignments (`developer`, `designer`, `lead_architect`, `admin`, etc.).
- **Project Management:** Project creation, retrieval, updates, and deletion with mandatory foreign-key existence validation on project owners.
- **Task Management:** Work item creation, assignment, priority scheduling, and due-date tracking linked directly to valid projects and users.
- **Dedicated Task Status Workflow:** Explicit status lifecycle (`todo` ➔ `in-progress` ➔ `done`) supported both via general updates and through a dedicated `PATCH /api/v1/tasks/{id}/status` endpoint.
- **Multi-Parameter Filtering:** Query parameters on tasks (`status`, `priority`, `project_id`, `assignee_id`) and projects (`status`, `owner_id`).
- **Standardized Pagination:** Predictable pagination metadata (`skip`, `limit`, `total`) with strict boundary validation (`skip >= 0`, `1 <= limit <= 100`).
- **Centralized Error Handling:** Uniform JSON error envelopes for domain exceptions, validation failures, HTTP errors, and unhandled exceptions without leaking stack traces.
- **Strict Input Validation:** Powered by Pydantic v2 schemas across all write operations.
- **Observability Headers:** Injects `X-Request-ID` correlation identifiers and `X-Process-Time` latency metrics on every HTTP response.
- **CORS Support:** Configurable cross-origin resource sharing allowing connection to the Week 1 React dashboard.
- **Pre-Seeded Development Dataset:** Pre-populates 4 users, 4 projects, and 11 tasks on application startup for immediate testing and demonstration.
- **Interactive OpenAPI Documentation:** Automatically generated Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## Tech Stack

- **Language:** Python 3.10+ (tested and verified on Python 3.14)
- **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (high-performance asynchronous web framework)
- **Data Validation & Serialization:** [Pydantic v2](https://docs.pydantic.dev/)
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
- **Testing Framework:** [pytest](https://pytest.org/)
- **HTTP Client for Testing:** [httpx](https://www.python-httpx.org/)

---

## Project Structure

The project follows a clean, modular layered architecture:

```
developer-productivity-api/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app factory, middleware, router inclusion & lifespan
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py            # API v1 aggregator router
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── users.py         # /api/v1/users endpoints
│   │       ├── projects.py      # /api/v1/projects endpoints
│   │       └── tasks.py         # /api/v1/tasks endpoints
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py            # Environment settings & .env parser
│   │   ├── exceptions.py        # Domain exceptions (ResourceNotFoundError, etc.)
│   │   └── error_handlers.py    # Centralized exception handlers for JSON error envelopes
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── common.py            # Common envelopes (DataResponse, PaginatedResponse, ErrorResponse)
│   │   ├── user.py              # User schemas, roles, and validators
│   │   ├── project.py           # Project schemas, statuses, and priorities
│   │   └── task.py              # Task schemas, status transitions, and priorities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User domain entity
│   │   ├── project.py           # Project domain entity
│   │   └── task.py              # Task domain entity
│   ├── data/
│   │   ├── __init__.py
│   │   ├── store.py             # Thread-safe in-memory store
│   │   └── seed.py              # Seed data generator (4 users, 4 projects, 11 tasks)
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py              # Base repository protocol
│   │   ├── user_repository.py   # User in-memory repository
│   │   ├── project_repository.py# Project in-memory repository
│   │   └── task_repository.py   # Task in-memory repository
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py      # User business logic & duplicate validation
│   │   ├── project_service.py   # Project business logic & owner existence checks
│   │   └── task_service.py      # Task business logic & relational verification
│   └── utils/
│       ├── __init__.py
│       └── ids.py               # Prefixed UUIDv4 generator
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest client fixtures and store isolation
│   ├── test_users.py            # User CRUD and validation tests
│   ├── test_projects.py         # Project CRUD and owner verification tests
│   ├── test_tasks.py            # Task CRUD, status updates, and relationship tests
│   ├── test_filters_and_pagination.py # Query filtering and pagination boundary tests
│   ├── test_errors.py           # Error envelopes, health checks, and observability tests
│   └── test_demo_workflow.py    # Full 13-step end-to-end user story test
├── main.py                  # Root entrypoint for Vercel deployment & ASGI discovery
├── docs/
│   └── api.md                   # Comprehensive API specification and endpoint guide
├── .env.example                 # Configuration template
├── .gitignore                   # Git ignore patterns
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

### Architectural Layering
1. **Routes (`app/api/routes`):** Handle HTTP transport, request extraction, query parameters, and serialization.
2. **Services (`app/services`):** Encapsulate business logic, enforce domain invariants (e.g. unique emails, existing project/assignee references), and coordinate actions.
3. **Repositories (`app/repositories`):** Abstract data persistence behind a standard interface. Swapping in-memory storage for an ORM in Week 3 requires changing only this layer.
4. **Data Store (`app/data`):** Manages entity storage, concurrency synchronization, and seed initialization.

---

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- Git

### 1. Clone Repository
```powershell
git clone https://github.com/Praveensagar07/developer-productivity-api.git
cd developer-productivity-api
```

### 2. Create Virtual Environment
#### Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### macOS / Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Copy `.env.example` to `.env`:
```powershell
copy .env.example .env
```

---

## Running the API

Start the development server with live reload:

```powershell
uvicorn app.main:app --reload --port 8000
```

Once running, access the services:
- **API Base:** `http://127.0.0.1:8000`
- **Health Check:** `http://127.0.0.1:8000/health`
- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

### Vercel Deployment Entrypoint
For serverless platforms such as Vercel, the root [`main.py`](main.py) re-exports the FastAPI application instance (`from app.main import app`) to ensure seamless ASGI discovery without modifying the internal layered `app/` package structure.

---

## API Endpoints

All primary resources are versioned under `/api/v1`.

| HTTP Method | Path | Summary | Success Code | Error Codes |
|:---|:---|:---|:---|:---|
| `GET` | `/` | API service information | `200` | — |
| `GET` | `/health` | Health status and timestamp | `200` | — |
| **Users** | | | | |
| `POST` | `/api/v1/users` | Register a new user | `201` | `400`, `409`, `422` |
| `GET` | `/api/v1/users` | List paginated users | `200` | `422` |
| `GET` | `/api/v1/users/{id}` | Get user by ID | `200` | `404` |
| `PATCH` | `/api/v1/users/{id}` | Update user fields | `200` | `404`, `409`, `422` |
| `DELETE` | `/api/v1/users/{id}` | Delete user | `200` | `404` |
| **Projects** | | | | |
| `POST` | `/api/v1/projects` | Create a new project | `201` | `404`, `422` |
| `GET` | `/api/v1/projects` | List paginated projects | `200` | `422` |
| `GET` | `/api/v1/projects/{id}` | Get project by ID | `200` | `404` |
| `PATCH` | `/api/v1/projects/{id}` | Update project fields | `200` | `404`, `422` |
| `DELETE` | `/api/v1/projects/{id}` | Delete project | `200` | `404` |
| **Tasks** | | | | |
| `POST` | `/api/v1/tasks` | Create a new task | `201` | `404`, `422` |
| `GET` | `/api/v1/tasks` | List tasks (with filters) | `200` | `422` |
| `GET` | `/api/v1/tasks/{id}` | Get task by ID | `200` | `404` |
| `PATCH` | `/api/v1/tasks/{id}` | Update task details | `200` | `404`, `422` |
| `PATCH` | `/api/v1/tasks/{id}/status` | Update task status | `200` | `404`, `422` |
| `DELETE` | `/api/v1/tasks/{id}` | Delete task | `200` | `404` |

*For complete schema specifications, sample payloads, and curl commands, see [docs/api.md](docs/api.md).*

---

## Validation & Business Invariants

Input validation is enforced using Pydantic models:
1. **Email Format & Uniqueness:** Validated via regex pattern (`^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`), trimmed, and normalized to lowercase. Creation of duplicate emails is rejected with `409 Conflict`.
2. **Non-Blank Fields:** Strings such as `name` and `title` reject whitespace-only values.
3. **Enum Verification:** Project status (`planning`, `active`, `completed`, `archived`), project priority (`low`, `medium`, `high`, `critical`), task status (`todo`, `in-progress`, `done`), and task priority are strictly checked against enum definitions.
4. **Relational Integrity:**
   - Projects cannot be created without a valid `owner_id` pointing to an existing user (`404 Not Found`).
   - Tasks cannot be created without a valid `project_id` pointing to an existing project (`404 Not Found`).
   - Tasks with an `assignee_id` must reference an existing user (`404 Not Found`).

---

## Centralized Error Handling

All error responses adhere to a consistent JSON structure:

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with id 'usr_nonexistent' was not found",
    "details": []
  }
}
```

For validation errors (`422 Unprocessable Entity`):
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "body.email",
        "message": "Email must be a valid email address (e.g., user@example.com)",
        "type": "value_error"
      }
    ]
  }
}
```

---

## Environment Variables

Settings are defined in `.env.example`:

| Variable | Default Value | Description |
|:---|:---|:---|
| `APP_NAME` | `Developer Productivity API` | API service name |
| `APP_ENV` | `development` | Environment mode (`development`, `production`, `test`) |
| `APP_VERSION` | `1.0.0` | Semantic API version |
| `DEBUG` | `true` | Debug mode toggle |
| `API_PREFIX` | `/api/v1` | URL prefix for versioned routes |
| `HOST` | `0.0.0.0` | Host interface for server binding |
| `PORT` | `8000` | Port for server binding |
| `CORS_ORIGINS` | `http://localhost:3000,http://localhost:5173,...` | Allowed CORS origins |
| `SEED_DATA_ON_STARTUP` | `true` | Load development mock data on startup |

---

## Automated Testing

The project includes an automated test suite with **37 tests** covering unit operations, business validation, filtering, pagination boundaries, and complete workflows.

To run the tests:

```powershell
python -m pytest tests/ -v
```

### Test Coverage Highlights:
- **`tests/test_users.py`:** User creation (201), duplicate email rejection (409), invalid email syntax (422), blank names (422), retrieval (200), not found (404), partial updates (200), and deletion (200).
- **`tests/test_projects.py`:** Project creation (201), non-existent owner rejection (404), pagination (200), retrieval (200), updates (200), and deletion (200).
- **`tests/test_tasks.py`:** Task creation (201), non-existent project rejection (404), non-existent assignee rejection (404), general updates (200), dedicated `/status` endpoint transitions (200), invalid status rejection (422), and deletion (200).
- **`tests/test_filters_and_pagination.py`:** Status filtering (`todo`, `in-progress`, `done`), priority filtering, project & assignee filtering, combined multi-filters, and pagination bounds checking.
- **`tests/test_errors.py`:** Standardized error envelopes, health check (`GET /health`), root info (`GET /`), and request correlation headers.
- **`tests/test_demo_workflow.py`:** Complete 13-step end-to-end integration workflow executing the entire project lifecycle in sequence.

---

## Demonstration Workflow

You can verify the entire workflow interactively via Swagger UI (`http://127.0.0.1:8000/docs`):

1. **POST** `/api/v1/users` ➔ Create Project Owner (`Alice Architect`)
2. **POST** `/api/v1/users` ➔ Create Assignee (`Bob Builder`)
3. **POST** `/api/v1/projects` ➔ Create Project owned by Alice
4. **POST** `/api/v1/tasks` ➔ Create Task under Project assigned to Bob (`status: todo`)
5. **GET** `/api/v1/tasks/{task_id}` ➔ Retrieve Task
6. **PATCH** `/api/v1/tasks/{task_id}/status` ➔ Move to `in-progress`
7. **PATCH** `/api/v1/tasks/{task_id}/status` ➔ Move to `done`
8. **GET** `/api/v1/tasks?status=done` ➔ Filter completed tasks
9. **PATCH** `/api/v1/tasks/{task_id}` ➔ Update Task priority to `critical`
10. **DELETE** `/api/v1/tasks/{task_id}` ➔ Delete Task
11. **GET** `/api/v1/tasks/{task_id}` ➔ Verify deletion (returns `404`)
12. **GET** `/api/v1/projects/{project_id}` ➔ Retrieve Project
13. **GET** `/api/v1/users` ➔ Retrieve Users collection
