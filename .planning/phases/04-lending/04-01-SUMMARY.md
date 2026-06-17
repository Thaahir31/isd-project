# Phase 4 Plan 1: Loan Request Workflow & Expiry Summary

Implemented the initial Loan Request workflow, allowing students to submit requests for books and librarians to manage them.

## Key Changes

### Models & Schemas
- Created `LoanRequest` model with `PENDING`, `APPROVED`, `DENIED`, and `EXPIRED` statuses.
- Added `created_at` and `expires_at` (default 3 days) fields to `LoanRequest`.
- Registered `LoanRequest` in `src/models/__init__.py`.
- Created `src/schemas/loan_request.py` for API data validation.

### API Endpoints
- `POST /api/loans/requests`: Allows students to request a book. Enforces a limit of 3 active requests/loans.
- `GET /api/loans/requests`: Allows librarians to list all pending requests.
- `POST /api/loans/requests/{id}/deny`: Allows librarians to deny a pending request.
- `POST /api/loans/requests/cleanup-expired`: Allows librarians to mark expired pending requests as `EXPIRED`.

### Database
- Generated and applied Alembic migration `160441597512_add_loan_requests_table.py`.

### Tests
- Created `tests/test_lending_requests.py` with 5 tests covering the implemented functionality.

## Verification Results
- All tests in `tests/test_lending_requests.py` passed.
- Student limit of 3 active items is enforced.
- Duplicate pending requests for the same book by the same student are prevented.
- RBAC is correctly applied to all endpoints.

## Self-Check: PASSED
- Created files exist: `src/models/loan_request.py`, `src/api/loans.py`, `src/schemas/loan_request.py`, `tests/test_lending_requests.py`, `alembic/versions/160441597512_add_loan_requests_table.py`.
- Commits exist: `6cadad7`.
