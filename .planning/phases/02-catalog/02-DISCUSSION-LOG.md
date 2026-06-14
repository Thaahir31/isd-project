# Phase 2 — Discussion Log: Catalog Management

## Session Date: 2026-06-14
**User Instruction:** "Use default values for all. Keep it simple."

## Decisions Summary
1. **ISBN:** Use ISBN-13 strings. Standard validation.
2. **Authors:** Stick to Many-to-One (one author per book) as per requirements.
3. **Fields:** Only include Title, Author, ISBN, Quantity, and Category.
4. **Search:** Implement fuzzy/partial search for Title and Author using ILIKE.
5. **Availability:** Persisted integer on Book model.

## Resolution
The phase will prioritize a clean, simple implementation of the catalog without advanced metadata or complex Many-to-Many relationships.
