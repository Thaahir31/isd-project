# Phase 2 — Context: Catalog Management

## F-001: Book CRUD (CATALOG-01)
- **ISBN:** ISBN-13 format, stored as a string. Required and unique.
- **Fields:** Title, Author (FK), ISBN, Quantity, Category.
- **Validation:** Standard ISBN-13 format validation.

## F-002: Author Management (CATALOG-02)
- **Relationship:** Many-to-One (One author per book).
- **Fields:** Name, Biography (optional).

## F-003: Search (CATALOG-03)
- **Scope:** Title, Author Name, ISBN.
- **Behavior:** Simple fuzzy/partial match (ILIKE) for Title and Author; Exact match for ISBN.
- **Performance Target:** < 1 second.

## F-004: Availability Tracking (CATALOG-04)
- **Logic:** Persisted `available_copies` count on the Book model.
- **Initial State:** `available_copies` equals `total_copies` upon book creation.

## Technical Decisions
- **Database:** PostgreSQL.
- **Search:** Native SQL `ILIKE` for simplicity in Phase 2.
- **Validation Library:** `python-stdnum` or regex for ISBN.
