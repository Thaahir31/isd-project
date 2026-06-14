# Phase 3 — Context: Member & Profile Management

## F-001: Member Registration (MEMBER-01)
- **Workflow:** Librarian-only registration via admin endpoint. No public sign-up.
- **Initial Password:** Provided by Librarian during creation.
- **Fields:** username, email, password, student_id, department, role (default: STUDENT).

## F-002: Profile Management (MEMBER-02, MEMBER-03)
- **View:** `/members/me` (Current user) and `/members/{id}` (Librarian access or Owner check).
- **Update Permissions:**
    - **Student:** Can update `phone_number` and `address`.
    - **Librarian:** Can update all fields, including `student_id`, `department`, and `role`.

## F-003: Borrow History (MEMBER-02)
- **Model:** Introduce `Loan` model now.
- **Fields:** id, book_id, user_id, status (Borrowed, Returned, Overdue), borrowed_at, returned_at, due_date.
- **API:** GET `/members/me/history` returns list of loans for the current student.

## Technical Decisions
- **Database:** Extend `User` table; Create `loans` table.
- **Security:** Ownership check on `/members/{id}` to ensure students only see their own data.
