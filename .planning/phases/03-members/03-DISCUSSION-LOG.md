# Phase 3 — Discussion Log: Member Management

## Session Date: 2026-06-14
**User Instruction:** "use defaults"

## Decisions Summary
1. **Registration:** Librarian-only. Simple password provisioning.
2. **Profile Fields:** Add `student_id`, `department`, `phone_number`.
3. **Permissions:** Split updates between Student (contact info) and Librarian (identity/role).
4. **History:** Create `Loan` model in this phase to support history endpoints ahead of Phase 4.

## Resolution
Phase 3 will build the user-centric features of the library, focusing on identity management and preparing the data structures needed for lending.
