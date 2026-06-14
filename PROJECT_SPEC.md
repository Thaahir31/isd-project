# Project Spec: Library Management System

## Core Value
Transform Universitas XYZ's manual paper-based library operations into a modern, web-based digital ecosystem, enabling real-time inventory tracking, secure role-based access, and efficient lending workflows.

## Success Criteria (v1)
- **Real-time Catalog:** Students can search and see accurate book availability in < 2 seconds.
- **Secure Access:** Clear distinction between Student and Librarian capabilities enforced via JWT.
- **Robust Lending:** Reliable borrow/return cycle with automated due date tracking and concurrency safety.
- **Operational Oversight:** Librarians have a real-time dashboard showing active loans and overdue items.

## Tech Stack
- **Language:** Python
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **Migrations:** Alembic
- **Infrastructure:** Docker & Docker Compose

## Core Features
1. **Foundation & Authentication:** Secure RBAC (Student/Librarian) and JWT-based auth.
2. **Catalog Management:** Full CRUD for Books and Authors with ISBN validation.
3. **Member Management:** Registration and profile management for students.
4. **Lending System:** Automated borrow/return state machine with concurrency protection.
5. **Admin Dashboard:** Operational reporting and statistics for librarians.

## Constraints
- API-first architecture.
- Must include comprehensive automated tests for the lending state machine.
- Must be deployable via a single `docker-compose up` command.

## Out of Scope
- Physical hardware integration (RFID/Barcodes).
- Payment processing for fines.
- Public-facing e-book reader.

## Project Structure
- `.planning/`: GSD workflow artifacts (Roadmap, Research, Requirements).
- `src/`: Application source code (to be created).
- `tests/`: Automated test suite (to be created).
