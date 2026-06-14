# Domain Pitfalls

**Domain:** Library Management System
**Researched:** 2026-12-06

## Critical Pitfalls

Mistakes that cause rewrites or major issues.

### Pitfall 1: Race Conditions in Borrowing
**What goes wrong:** Two users request the last copy of a book at the exact same millisecond. Both requests are processed, and the library "over-lends."
**Why it happens:** Reading availability and decrementing the count are not atomic operations.
**Consequences:** Negative inventory; librarians have to explain to a student why their "approved" book isn't on the shelf.
**Prevention:** Use database transactions with proper isolation levels (e.g., `SELECT ... FOR UPDATE` in PostgreSQL) to lock the row during the borrow transaction.
**Detection:** Integration tests that simulate concurrent borrow requests.

### Pitfall 2: Neglecting ISBN-13 Transition
**What goes wrong:** Database fields for ISBN are too short or validation logic fails for modern ISBN-13 codes.
**Why it happens:** Using older standards or strict 10-digit validation logic.
**Prevention:** Use a flexible string field for ISBN (13+ characters) and use a library like `python-stdnum` for validation.

## Moderate Pitfalls

### Pitfall 1: Hardcoding Fine Logic
**What goes wrong:** Library changes its policy (e.g., goes "fine-free"), but the logic is hardcoded deep in the return service.
**Prevention:** Store fine rates/rules in a configuration table or environment variables.

### Pitfall 2: Inefficient Search
**What goes wrong:** As the catalog grows to 50k+ books, `SELECT * FROM books WHERE title LIKE '%...%'` becomes painfully slow.
**Prevention:** Implement indexing on search columns and consider PostgreSQL Full-Text Search (FTS) early.

## Minor Pitfalls

### Pitfall 1: Poor Date Handling
**What goes wrong:** Timezone mismatches cause books to be marked overdue a day early or late.
**Prevention:** Always use UTC in the database and convert to local time only in the UI.

## Phase-Specific Warnings

| Phase Topic | Likely Pitfall | Mitigation |
|-------------|---------------|------------|
| Database Schema | Missing `AvailableCopies` | Ensure inventory logic is separate from total count. |
| Authentication | Role Leakage | Explicitly check roles on every "Librarian-only" endpoint. |
| Borrowing | Unlimited Loans | Implement a "Max Loans" per user config from the start. |

## Sources

- [StackOverflow: Handling concurrency in library management system](https://stackoverflow.com)
- [Post-mortem: Why "Fine Free" is the new standard](https://galecia.com)
