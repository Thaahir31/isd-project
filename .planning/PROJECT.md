# Project: Library Management System

## Core Value
Transform Universitas XYZ's manual paper-based library operations into a modern, web-based digital ecosystem, enabling real-time inventory tracking, secure role-based access, and efficient lending workflows.

## Success Criteria (v1)
- **Real-time Catalog:** Students can search and see accurate book availability in < 2 seconds.
- **Secure Access:** Clear distinction between Student and Librarian capabilities enforced via JWT.
- **Robust Lending:** Reliable borrow/return cycle with automated due date tracking and concurrency safety.
- **Operational Oversight:** Librarians have a real-time dashboard showing active loans and overdue items.

## Constraints
- **Stack:** FastAPI (Python), PostgreSQL, Docker.
- **Environment:** Must deploy cleanly via Docker Compose.
- **Scope:** API-first backend (Backend emphasis).
- **Out of Scope:** Payments, E-books, Native apps.

## Key Stakeholders
- **Librarians:** Owners of the catalog and lending decisions.
- **Students:** Consumers of the library collection.
- **IT Department:** Infrastructure and deployment managers.

## References
- Research Findings: `.planning/research/`
- Original Spec: `sample-project/library-management/PROJECT_SPEC.md`
