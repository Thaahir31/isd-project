# Phase 4 — Context: Lending Logic & Concurrency

## F-001: Borrowing Workflow (LENDING-01)
- **Process:**
  1. Student submits a "Loan Request" for a specific book.
  2. Request is visible to Librarians in a pending state.
  3. Librarian can **Approve** (starts the loan) or **Deny** (cancels the request) the request.
- **Request Expiry:** Pending requests automatically expire after **3 days** if no action is taken.
- **Loan Policy:**
  - **Default Duration:** 14 calendar days.
  - **Limit:** Maximum of **3 active loans/requests** per student at any time.

## F-002: Return Workflow (LENDING-02)
- **Librarian Action:** Librarian records the return of a physical book.
- **Features:**
  - **Condition Tracking:** Option to mark book condition (Good, Damaged, Lost) during return.
  - **Fine Calculation:** System calculates fines for overdue returns.
  - **Notifications:** Trigger a stub/placeholder notification to the student upon successful return.

## F-003: Concurrency & Integrity (LENDING-03)
- **Strategy:** Use **Pessimistic Locking** (`SELECT FOR UPDATE`) at the database level.
- **Target:** When a loan is being approved or a direct loan is created, lock the book inventory record to ensure `available_copies > 0` before decrementing.

## F-004: Fine Management
- **Daily Rate:** $0.50 per day overdue.
- **Calculation:** (Current Date - Due Date) * $0.50. Only applies if Current Date > Due Date.

## Technical Decisions
- **Models:** 
  - `LoanRequest` (id, user_id, book_id, status, created_at, expires_at)
  - `Loan` (id, user_id, book_id, borrowed_at, due_date, returned_at, condition, total_fine, status)
- **Status Enum:** `PENDING`, `APPROVED`, `DENIED`, `EXPIRED`, `ACTIVE`, `RETURNED`, `OVERDUE`.
