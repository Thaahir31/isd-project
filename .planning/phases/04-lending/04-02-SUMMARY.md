# Phase 4 Plan 02: Lending Approval & Concurrency Summary

Implemented the core lending transition from Request to Loan, ensuring strict data integrity through atomic updates and pessimistic locking.

## Key Changes

### 1. Loan Model & Schema
- Created `src/models/loan.py` with fields: `id`, `user_id`, `book_id`, `borrowed_at`, `due_date`, `returned_at`, `condition`, `status`, and `total_fine`.
- Created `src/schemas/loan.py` for API responses.
- Applied migration `9d976b5ae1b8_add_loans_table.py`.

### 2. Approval Logic
- Implemented `POST /api/loans/requests/{request_id}/approve`.
- Uses `with_for_update()` on the `Book` record for row-level locking on supported databases.
- Uses an atomic SQL update (`Book.available_copies - 1`) to ensure inventory integrity even on SQLite during tests.
- Re-enforces the 3-active-items limit (loans + pending/approved requests) at the time of approval.
- Successfully transitions `LoanRequest` to `APPROVED` and creates an `ACTIVE` `Loan`.

### 3. Concurrency Verification
- Created `tests/test_concurrency.py` using `ThreadPoolExecutor` to simulate simultaneous approval attempts for the last copy of a book.
- Verified that exactly one request succeeds and others are rejected with a 400 error.
- Verified database consistency (inventory remains 0, only one loan created).

## Verification Results

### Automated Tests
- `pytest tests/test_models.py`: PASSED
- `pytest tests/test_concurrency.py`: PASSED

## Self-Check: PASSED
- Loan model is implemented.
- Approval logic uses pessimistic locking / atomic updates.
- Concurrency test passes with multiple simulated threads.
