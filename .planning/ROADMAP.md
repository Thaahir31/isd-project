# Roadmap: Library Management System

## Phases

- [x] **Phase 1: Foundation & Authentication** - Establish secure core and user roles.
- [x] **Phase 2: Catalog Management** - Manage and search the physical inventory.
- [ ] **Phase 3: Member & Profile Management** - Manage library members and their access.
- [ ] **Phase 4: Lending Logic & Concurrency** - Enable borrowing/returning with data integrity.
- [ ] **Phase 5: Admin Dashboard & Statistics** - Provide operational oversight for librarians.

## Phase Details

### Phase 1: Foundation & Authentication
**Goal**: Establish the secure technical core and identity management.
**Depends on**: Nothing
**Requirements**: SETUP-01, SETUP-02, SETUP-03, SETUP-04, AUTH-01, AUTH-02, AUTH-03
**Success Criteria** (what must be TRUE):
  1. API shell is responsive and database migrations are working via Alembic.
  2. A "Librarian" user can log in and receive a JWT token.
  3. Non-authenticated users cannot access restricted Librarian endpoints.
  4. Docker Compose environment starts all services (DB, API) with one command.
**Plans**:
- [x] 01-01-PLAN.md — Project Skeleton & Environment (FastAPI, Docker, SQLAlchemy)
- [x] 01-02-PLAN.md — Authentication & Role Management (JWT, RBAC, Seed Script)
- [x] 01-03-PLAN.md — Testing Infrastructure (Pytest, Integration Tests)

### Phase 2: Catalog Management
**Goal**: Build the searchable book inventory with Author management and availability tracking.
**Depends on**: Phase 1
**Requirements**: CATALOG-01, CATALOG-02, CATALOG-03, CATALOG-04
**Success Criteria** (what must be TRUE):
  1. Librarian can perform CRUD operations on Books and Authors via API.
  2. Search endpoint returns relevant results by Title, Author, or ISBN in < 1s.
  3. Every book record shows correct "total" vs "available" quantity.
**Plans**:
- [x] 02-01-PLAN.md — Catalog Foundation (Models & Authors)
- [x] 02-02-PLAN.md — Book Management (CRUD & ISBN Validation)
- [x] 02-03-PLAN.md — Search & Availability Tracking

### Phase 3: Member & Profile Management
**Goal**: Manage user identities beyond authentication.
**Depends on**: Phase 1
**Requirements**: MEMBER-01, MEMBER-02, MEMBER-03
**Success Criteria** (what must be TRUE):
  1. Librarian can register a new student and assign library privileges.
  2. Student can view their own borrow history and current contact info.
**Plans**:
- [ ] 03-01-PLAN.md — Member Registration & Roles
- [ ] 03-02-PLAN.md — Student Profiles & History

### Phase 4: Lending Logic & Concurrency
**Goal**: Implement the core borrow/return state machine with high integrity.
**Depends on**: Phase 2, Phase 3
**Requirements**: LENDING-01, LENDING-02, LENDING-03, LENDING-04
**Success Criteria** (what must be TRUE):
  1. A student can request a book and the request appears for librarians.
  2. Librarian can approve a request, creating an "Active" loan with a calculated due date.
  3. System prevents lending the same physical copy to two people simultaneously (verified via concurrency test).
  4. Librarian can record a return, which automatically restores book availability.
**Plans**:
- [ ] 04-01-PLAN.md — Loan Request Workflow & Expiry
- [ ] 04-02-PLAN.md — Loan Management & Concurrency
- [ ] 04-03-PLAN.md — Return Logic & Fine Calculation

### Phase 5: Admin Dashboard & Statistics
**Goal**: Provide operational oversight for librarians.
**Depends on**: Phase 4
**Requirements**: ADMIN-01, ADMIN-02, ADMIN-03
**Success Criteria** (what must be TRUE):
  1. Dashboard API returns correct counts for total books, active loans, and pending requests.
  2. Librarian can pull a list of all "Overdue" loans for immediate action.
  3. All lending actions are recorded in an audit log for accountability.
**Plans**: TBD
**UI hint**: yes

## Progress Table

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation & Auth | 3/3 | Completed | 2026-06-12 |
| 2. Catalog Management | 3/3 | Completed | 2026-06-14 |
| 3. Member Management | 0/2 | Discussed | - |
| 4. Lending Logic | 0/3 | Planned | - |
| 5. Admin Dashboard | 0/1 | Not started | - |
