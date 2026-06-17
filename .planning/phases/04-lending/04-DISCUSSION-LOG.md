# Phase 4 — Discussion Log: Lending Logic & Concurrency

## Session Date: 2026-06-15

### Question 1: Borrowing Workflow
- **Agent:** How should the borrowing process start?
- **User:** Request -> Approval (Student requests via API, Librarian approves).
- **Resolution:** Implemented as a two-stage workflow with `LoanRequest` and `Loan` entities.

### Question 2: Loan Policy & Limits
- **Agent:** What is the default loan duration and is there a limit on active loans?
- **User:** 14 days, max 3 books, yes auto expire [requests] after 3 days.
- **Resolution:** Set default duration to 14 calendar days. Capped active loans/requests at 3. Added 3-day TTL for pending requests.

### Question 3: Concurrency Handling
- **Agent:** How should we handle the race condition where two people try to borrow the last copy simultaneously?
- **User:** Pessimistic Locking (DB) (SELECT FOR UPDATE).
- **Resolution:** Adopted pessimistic locking strategy for inventory updates.

### Question 4: Return Workflow & Fines
- **Agent:** What should happen when a book is returned?
- **User:** Overdue Fines, Condition Tracking, Return Notification.
- **Resolution:** Added fields for book condition and fine tracking. Stubbed notification system.

### Question 5: Fine Configuration & Calendar
- **Agent:** What is the daily fine rate and how is the duration calculated?
- **User:** $0.50 per day, Calendar Days.
- **Resolution:** Fixed fine rate at $0.50/day. Calculation based on calendar days (including weekends).
