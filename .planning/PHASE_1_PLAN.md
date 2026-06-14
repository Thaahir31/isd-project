# Phase 1 Execution Plan: Foundation & Authentication

**Phase Goal**: Establish secure technical core and identity management for the Library Management System.

## Wave Structure

| Wave | Plans | Autonomous | Key Objectives |
|------|-------|------------|----------------|
| 1 | 01-01 | Yes | FastAPI Skeleton, Docker, SQLAlchemy, Alembic |
| 2 | 01-02, 01-03 | Yes | JWT Auth, RBAC, Seed Librarian, Pytest Setup |

## Plan Summaries

### [01-01] Project Skeleton & Environment
- **Objective**: Initialize the containerized FastAPI environment with database connectivity.
- **Requirements**: SETUP-01, SETUP-02, SETUP-03
- **Tasks**:
  1. **Initialize Project & Docker**: Create Dockerfile, docker-compose.yml, main.py (health-check).
  2. **Configure SQLAlchemy & Alembic**: Setup DB engine and migration framework.
- **Files**: `Dockerfile`, `docker-compose.yml`, `requirements.txt`, `src/main.py`, `src/database.py`, `alembic/`

### [01-02] Authentication & Role Management
- **Objective**: Implement JWT-based identity and role-based access control.
- **Requirements**: AUTH-01, AUTH-02, AUTH-03
- **Tasks**:
  1. **JWT Auth Logic**: User model (Student/Librarian roles), Login endpoint, JWT generation.
  2. **RBAC & Seed**: Implement role-check middleware and seed the first Librarian user.
- **Files**: `src/models/user.py`, `src/auth.py`, `src/api/auth.py`, `scripts/seed_librarian.py`

### [01-03] Testing Infrastructure
- **Objective**: Setup the automated quality gate for the project.
- **Requirements**: SETUP-04
- **Tasks**:
  1. **Pytest Setup**: Configure conftest.py and health-check tests.
  2. **Auth Integration Tests**: Verify login and RBAC logic.
- **Files**: `tests/conftest.py`, `tests/test_main.py`, `tests/test_auth.py`

## Goal-Backward Verification (Must-Haves)

### Observable Truths
- `docker compose up` starts all services without error.
- `GET /health` returns `{"status": "ok"}`.
- `POST /auth/login` returns a valid JWT for the seeded Librarian.
- `GET /auth/librarian-only` returns 200 for Librarians and 403 for Students.
- `pytest` runs and passes all core foundation tests.

### Key Links
- **API → DB**: Verified via Alembic migration and health-check.
- **Auth → JWT**: Verified via login endpoint.
- **RBAC → API**: Verified via protected test endpoints.

---
*Note: This consolidated plan is derived from the GSD-structured plans located in `.planning/phases/01-foundation-auth/`.*
