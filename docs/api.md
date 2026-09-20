# Developer Productivity REST API — Specification & Documentation

> **Innovation Hacks Full Stack Development Internship — Week 2 / Task 2**  
> **Service:** Users, Projects & Tasks REST API  
> **Base URL:** `http://127.0.0.1:8000/api/v1`  
> **Interactive Swagger UI:** `http://127.0.0.1:8000/docs`  
> **Interactive ReDoc:** `http://127.0.0.1:8000/redoc`

---

## Table of Contents
1. [Global Conventions & Envelopes](#global-conventions--envelopes)
2. [User Management Endpoints](#1-user-management-endpoints)
3. [Project Management Endpoints](#2-project-management-endpoints)
4. [Task Management Endpoints](#3-task-management-endpoints)
5. [Filtering Guide](#4-filtering-guide)
6. [Pagination Guide](#5-pagination-guide)
7. [Error Responses & Formats](#6-error-responses--formats)
8. [HTTP Status Codes Reference](#7-http-status-codes-reference)
9. [Complete 13-Step Workflow Walkthrough](#8-complete-13-step-workflow-walkthrough)

---

## Global Conventions & Envelopes

All successful responses return JSON wrapped in predictable envelopes:
- **Single Resource:** `{"data": { ... }}`
- **Paginated Collection:** `{"data": [ ... ], "meta": { "total": int, "skip": int, "limit": int }}`
- **Confirmation / Deletion:** `{"data": { "message": str, "id": str }}`
- **Error:** `{"error": { "code": str, "message": str, "details": [ ... ] }}`

Every response includes observability headers:
- `X-Request-ID`: Correlation identifier for request tracing.
- `X-Process-Time`: Server round-trip processing time in milliseconds (e.g. `2.45ms`).

---

## 1. User Management Endpoints

### 1.1 Create User
- **Method & Path:** `POST /api/v1/users`
- **Status Code:** `201 Created`
- **Description:** Creates a new user. Rejects empty names and invalid/duplicate emails.

#### Request Body
```json
{
  "name": "Sarah Connor",
  "email": "sarah.connor@example.com",
  "role": "developer"
}
```
*Roles supported: `developer`, `designer`, `product_manager`, `qa_engineer`, `lead_architect`, `admin` (default: `developer`).*

#### Response (`201 Created`)
```json
{
  "data": {
    "id": "usr_9a8b7c6d5e4f",
    "name": "Sarah Connor",
    "email": "sarah.connor@example.com",
    "role": "developer",
    "created_at": "2026-09-20T11:45:00.000000Z",
    "updated_at": "2026-09-20T11:45:00.000000Z"
  }
}
```

---

### 1.2 List Users
- **Method & Path:** `GET /api/v1/users`
- **Status Code:** `200 OK`
- **Query Parameters:**
  - `skip` *(int, default 0, ge=0)*: Number of users to skip.
  - `limit` *(int, default 20, 1..100)*: Max users to return.
  - `role` *(string, optional)*: Filter by user role.

#### Response (`200 OK`)
```json
{
  "data": [
    {
      "id": "usr_alex_rivera",
      "name": "Alex Rivera",
      "email": "alex.rivera@example.com",
      "role": "admin",
      "created_at": "2026-09-06T11:45:00.000000Z",
      "updated_at": "2026-09-06T11:45:00.000000Z"
    }
  ],
  "meta": {
    "total": 1,
    "skip": 0,
    "limit": 20
  }
}
```

---

### 1.3 Get User by ID
- **Method & Path:** `GET /api/v1/users/{user_id}`
- **Status Code:** `200 OK` (or `404 Not Found`)

#### Response (`200 OK`)
```json
{
  "data": {
    "id": "usr_alex_rivera",
    "name": "Alex Rivera",
    "email": "alex.rivera@example.com",
    "role": "admin",
    "created_at": "2026-09-06T11:45:00.000000Z",
    "updated_at": "2026-09-06T11:45:00.000000Z"
  }
}
```

---

### 1.4 Update User
- **Method & Path:** `PATCH /api/v1/users/{user_id}`
- **Status Code:** `200 OK` (or `404 Not Found` / `409 Conflict`)
- **Description:** Partially updates user attributes (`name`, `email`, `role`).

#### Request Body
```json
{
  "name": "Alex Rivera-Soto",
  "role": "lead_architect"
}
```

#### Response (`200 OK`)
```json
{
  "data": {
    "id": "usr_alex_rivera",
    "name": "Alex Rivera-Soto",
    "email": "alex.rivera@example.com",
    "role": "lead_architect",
    "created_at": "2026-09-06T11:45:00.000000Z",
    "updated_at": "2026-09-20T11:45:10.000000Z"
  }
}
```

---

### 1.5 Delete User
- **Method & Path:** `DELETE /api/v1/users/{user_id}`
- **Status Code:** `200 OK` (or `404 Not Found`)

#### Response (`200 OK`)
```json
{
  "data": {
    "message": "User deleted successfully",
    "id": "usr_alex_rivera"
  }
}
```

---

## 2. Project Management Endpoints

### 2.1 Create Project
- **Method & Path:** `POST /api/v1/projects`
- **Status Code:** `201 Created` (or `404 Not Found` if `owner_id` is invalid)
- **Description:** Creates a new project owned by an existing user.

#### Request Body
```json
{
  "name": "Developer Productivity Dashboard",
  "description": "Unified metrics and task tracking frontend platform.",
  "status": "active",
  "priority": "critical",
  "owner_id": "usr_alex_rivera"
}
```
*Statuses supported: `planning`, `active`, `completed`, `archived`.*  
*Priorities supported: `low`, `medium`, `high`, `critical`.*

#### Response (`201 Created`)
```json
{
  "data": {
    "id": "prj_1a2b3c4d5e6f",
    "name": "Developer Productivity Dashboard",
    "description": "Unified metrics and task tracking frontend platform.",
    "status": "active",
    "priority": "critical",
    "owner_id": "usr_alex_rivera",
    "created_at": "2026-09-20T11:45:00.000000Z",
    "updated_at": "2026-09-20T11:45:00.000000Z"
  }
}
```

---

### 2.2 List Projects
- **Method & Path:** `GET /api/v1/projects`
- **Status Code:** `200 OK`
- **Query Parameters:**
  - `skip` *(int, default 0, ge=0)*
  - `limit` *(int, default 20, 1..100)*
  - `owner_id` *(string, optional)*: Filter by owner user ID.
  - `status` *(string, optional)*: Filter by lifecycle status.

#### Response (`200 OK`)
```json
{
  "data": [
    {
      "id": "prj_dev_dashboard",
      "name": "Developer Productivity Dashboard",
      "description": "Modern unified metrics, work analytics, and task tracking frontend platform.",
      "status": "active",
      "priority": "critical",
      "owner_id": "usr_alex_rivera",
      "created_at": "2026-09-06T11:45:00.000000Z",
      "updated_at": "2026-09-15T11:45:00.000000Z"
    }
  ],
  "meta": {
    "total": 4,
    "skip": 0,
    "limit": 20
  }
}
```

---

### 2.3 Get Project by ID
- **Method & Path:** `GET /api/v1/projects/{project_id}`
- **Status Code:** `200 OK` (or `404 Not Found`)

---

### 2.4 Update Project
- **Method & Path:** `PATCH /api/v1/projects/{project_id}`
- **Status Code:** `200 OK` (or `404 Not Found` if project or new `owner_id` not found)

#### Request Body
```json
{
  "status": "completed",
  "priority": "medium"
}
```

---

### 2.5 Delete Project
- **Method & Path:** `DELETE /api/v1/projects/{project_id}`
- **Status Code:** `200 OK` (or `404 Not Found`)

---

## 3. Task Management Endpoints

### 3.1 Create Task
- **Method & Path:** `POST /api/v1/tasks`
- **Status Code:** `201 Created` (or `404 Not Found` if `project_id` or `assignee_id` do not exist)

#### Request Body
```json
{
  "title": "Build centralized error handlers",
  "description": "Standardize JSON envelopes across domain exceptions.",
  "project_id": "prj_dev_dashboard",
  "assignee_id": "usr_jordan_lee",
  "status": "todo",
  "priority": "high",
  "due_date": "2026-09-28T18:00:00Z"
}
```
*Statuses supported: `todo`, `in-progress`, `done`.*  
*Priorities supported: `low`, `medium`, `high`, `critical`.*

#### Response (`201 Created`)
```json
{
  "data": {
    "id": "tsk_7a6b5c4d3e2f",
    "title": "Build centralized error handlers",
    "description": "Standardize JSON envelopes across domain exceptions.",
    "project_id": "prj_dev_dashboard",
    "assignee_id": "usr_jordan_lee",
    "status": "todo",
    "priority": "high",
    "due_date": "2026-09-28T18:00:00Z",
    "created_at": "2026-09-20T11:45:00.000000Z",
    "updated_at": "2026-09-20T11:45:00.000000Z"
  }
}
```

---

### 3.2 List Tasks
- **Method & Path:** `GET /api/v1/tasks`
- **Status Code:** `200 OK`
- **Query Parameters:**
  - `skip` *(int, default 0, ge=0)*
  - `limit` *(int, default 20, 1..100)*
  - `status` *(string, optional)*: Filter by status (`todo`, `in-progress`, `done`).
  - `priority` *(string, optional)*: Filter by priority (`low`, `medium`, `high`, `critical`).
  - `project_id` *(string, optional)*: Filter by parent project.
  - `assignee_id` *(string, optional)*: Filter by assignee user.

---

### 3.3 Get Task by ID
- **Method & Path:** `GET /api/v1/tasks/{task_id}`
- **Status Code:** `200 OK` (or `404 Not Found`)

---

### 3.4 Update Task (General)
- **Method & Path:** `PATCH /api/v1/tasks/{task_id}`
- **Status Code:** `200 OK` (or `404 Not Found`)

#### Request Body
```json
{
  "title": "Build centralized error handlers & logging",
  "priority": "critical"
}
```

---

### 3.5 Update Task Status (Dedicated Workflow Endpoint)
- **Method & Path:** `PATCH /api/v1/tasks/{task_id}/status`
- **Status Code:** `200 OK` (or `404 Not Found` / `422 Unprocessable Entity`)
- **Description:** Streamlined dedicated endpoint specifically designed for board card state dragging and status transitions (`todo` -> `in-progress` -> `done`).

#### Request Body
```json
{
  "status": "in-progress"
}
```

#### Response (`200 OK`)
```json
{
  "data": {
    "id": "tsk_7a6b5c4d3e2f",
    "title": "Build centralized error handlers",
    "description": "Standardize JSON envelopes across domain exceptions.",
    "project_id": "prj_dev_dashboard",
    "assignee_id": "usr_jordan_lee",
    "status": "in-progress",
    "priority": "high",
    "due_date": "2026-09-28T18:00:00Z",
    "created_at": "2026-09-20T11:45:00.000000Z",
    "updated_at": "2026-09-20T11:46:00.000000Z"
  }
}
```

---

### 3.6 Delete Task
- **Method & Path:** `DELETE /api/v1/tasks/{task_id}`
- **Status Code:** `200 OK` (or `404 Not Found`)

#### Response (`200 OK`)
```json
{
  "data": {
    "message": "Task deleted successfully",
    "id": "tsk_7a6b5c4d3e2f"
  }
}
```

---

## 4. Filtering Guide

Tasks and projects support multi-parameter filtering directly via query string:

### Filter Tasks by Status
```http
GET /api/v1/tasks?status=in-progress
```

### Filter Tasks by Priority
```http
GET /api/v1/tasks?priority=critical
```

### Filter Tasks by Project and Assignee
```http
GET /api/v1/tasks?project_id=prj_dev_dashboard&assignee_id=usr_samira_khan
```

### Combined Filter with Pagination
```http
GET /api/v1/tasks?project_id=prj_dev_dashboard&status=done&priority=high&skip=0&limit=10
```

---

## 5. Pagination Guide

All collection listing endpoints (`/users`, `/projects`, `/tasks`) support pagination using offset-limit semantics:
- `skip`: Number of records to skip from the start (default `0`, must be `>= 0`).
- `limit`: Number of records to return (default `20`, minimum `1`, maximum `100`).

Example request:
```http
GET /api/v1/tasks?skip=20&limit=10
```

Metadata object returned:
```json
{
  "data": [ ... ],
  "meta": {
    "total": 45,
    "skip": 20,
    "limit": 10
  }
}
```

---

## 6. Error Responses & Formats

The API enforces a standardized error structure across all HTTP failure codes.

### 404 Resource Not Found
```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "User with id 'usr_nonexistent' was not found",
    "details": []
  }
}
```

### 409 Duplicate Resource
```json
{
  "error": {
    "code": "DUPLICATE_RESOURCE",
    "message": "A user with email 'sarah.connor@example.com' already exists",
    "details": []
  }
}
```

### 422 Request Validation Error
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

## 7. HTTP Status Codes Reference

| Status Code | Reason Phrase | Typical Scenario in Productivity API |
|:---|:---|:---|
| `200` | OK | Successful GET, PATCH, DELETE operations. |
| `201` | Created | Successfully created user, project, or task. |
| `400` | Bad Request | Operation violates domain invariant. |
| `404` | Not Found | Requested entity or referenced foreign key (owner/project/assignee) does not exist. |
| `409` | Conflict | Attempted to register duplicate unique field (e.g. existing email). |
| `422` | Unprocessable Entity | Input payload failed Pydantic validation (e.g., blank string, malformed email, enum violation). |
| `500` | Internal Server Error | Unhandled unexpected server error (sanitized envelope returned). |

---

## 8. Complete 13-Step Workflow Walkthrough

Use this step-by-step sequence in Swagger UI (`/docs`) or curl to demonstrate the complete full-stack backend lifecycle:

1. **Create User A (Project Owner):**
   ```http
   POST /api/v1/users
   Content-Type: application/json

   { "name": "Alice Architect", "email": "alice@example.com", "role": "lead_architect" }
   ```
2. **Create User B (Assignee):**
   ```http
   POST /api/v1/users
   Content-Type: application/json

   { "name": "Bob Builder", "email": "bob@example.com", "role": "developer" }
   ```
3. **Create Project Owned by User A:**
   ```http
   POST /api/v1/projects
   Content-Type: application/json

   { "name": "Platform Microservices", "owner_id": "<USER_A_ID>" }
   ```
4. **Create Task under that Project & Assign to User B:**
   ```http
   POST /api/v1/tasks
   Content-Type: application/json

   { "title": "Build Auth Router", "project_id": "<PROJECT_ID>", "assignee_id": "<USER_B_ID>", "status": "todo" }
   ```
5. **Retrieve the Created Task:**
   ```http
   GET /api/v1/tasks/<TASK_ID>
   ```
6. **Advance Task Status to `in-progress`:**
   ```http
   PATCH /api/v1/tasks/<TASK_ID>/status
   Content-Type: application/json

   { "status": "in-progress" }
   ```
7. **Complete Task Status to `done`:**
   ```http
   PATCH /api/v1/tasks/<TASK_ID>/status
   Content-Type: application/json

   { "status": "done" }
   ```
8. **Filter Tasks by Project & Status:**
   ```http
   GET /api/v1/tasks?project_id=<PROJECT_ID>&status=done
   ```
9. **Update Task Priority / Details:**
   ```http
   PATCH /api/v1/tasks/<TASK_ID>
   Content-Type: application/json

   { "priority": "critical" }
   ```
10. **Delete the Task:**
    ```http
    DELETE /api/v1/tasks/<TASK_ID>
    ```
11. **Verify Task Deletion:**
    ```http
    GET /api/v1/tasks/<TASK_ID>
    ```
    *(Expects 404 RESOURCE_NOT_FOUND)*
12. **Retrieve Project:**
    ```http
    GET /api/v1/projects/<PROJECT_ID>
    ```
13. **Retrieve Users:**
    ```http
    GET /api/v1/users
    ```
