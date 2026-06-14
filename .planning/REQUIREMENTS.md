# Requirements: Library Management System

## Status
**Total Requirements:** 20
**Mapped:** 0 (0.0%)
**Completed:** 0 (0.0%)

## v1 Requirements

### Foundation (SETUP)
- **SETUP-01**: Initialize FastAPI project structure with standard GSD layout.
- **SETUP-02**: Configure PostgreSQL database with SQLAlchemy ORM and Alembic migrations.
- **SETUP-03**: Containerize application using Docker and Docker Compose.
- **SETUP-04**: Implement automated testing suite (pytest).

### Authentication & Authorization (AUTH)
- **AUTH-01**: Implement JWT-based authentication for user login.
- **AUTH-02**: Define Role-Based Access Control (RBAC) with Student and Librarian roles.
- **AUTH-03**: Secure endpoints based on user roles (e.g., Librarian-only book management).

### Catalog Management (CATALOG)
- **CATALOG-01**: CRUD operations for Books (Title, Author, ISBN, Quantity, Category).
- **CATALOG-02**: Manage Author entities with one-to-many relationship to Books.
- **CATALOG-03**: Implement full-text search for the catalog (Title, Author, ISBN).
- **CATALOG-04**: Track real-time availability of books based on current inventory and active loans.

### Member Management (MEMBER)
- **MEMBER-01**: Librarian capability to register and manage student accounts.
- **MEMBER-02**: Student capability to view their own profile and borrow history.
- **MEMBER-03**: Profile updates for contact information and preferences.

### Lending Logic (LENDING)
- **LENDING-01**: Borrowing workflow: Student requests book -> Librarian approves/denies.
- **LENDING-02**: Return workflow: Librarian records return -> Book availability updates.
- **LENDING-03**: Prevent race conditions in borrowing using database transactions (SELECT FOR UPDATE).
- **LENDING-04**: Automatic due date calculation and status tracking (Active, Overdue, Returned).

### Admin & Statistics (ADMIN)
- **ADMIN-01**: Dashboard API providing statistics on total books, active loans, and pending requests.
- **ADMIN-02**: Overdue book reporting and list management for Librarians.
- **ADMIN-03**: Audit logs for borrowing/returning activities.

## v2 Requirements (Out of Scope)
- Online fine payment.
- E-book delivery/streaming.
- Inter-library loans.
- Native mobile applications.

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| SETUP-01 | Phase 1 | Pending |
| SETUP-02 | Phase 1 | Pending |
| SETUP-03 | Phase 1 | Pending |
| SETUP-04 | Phase 1 | Pending |
| AUTH-01 | Phase 1 | Pending |
| AUTH-02 | Phase 1 | Pending |
| AUTH-03 | Phase 1 | Pending |
| CATALOG-01 | Phase 2 | Pending |
| CATALOG-02 | Phase 2 | Pending |
| CATALOG-03 | Phase 2 | Pending |
| CATALOG-04 | Phase 2 | Pending |
| MEMBER-01 | Phase 3 | Pending |
| MEMBER-02 | Phase 3 | Pending |
| MEMBER-03 | Phase 3 | Pending |
| LENDING-01 | Phase 4 | Pending |
| LENDING-02 | Phase 4 | Pending |
| LENDING-03 | Phase 4 | Pending |
| LENDING-04 | Phase 4 | Pending |
| ADMIN-01 | Phase 5 | Pending |
| ADMIN-02 | Phase 5 | Pending |
| ADMIN-03 | Phase 5 | Pending |
