# Feature Landscape

**Domain:** Library Management System
**Researched:** 2026-12-06

## Table Stakes

Features users expect. Missing = product feels incomplete.

| Feature | Why Expected | Complexity | Notes |
|---------|--------------|------------|-------|
| Book Catalog Search | Essential for finding books. | Low | Search by title, author, ISBN. |
| User Authentication | Security and identity. | Medium | JWT-based login (Student/Librarian). |
| Borrowing Workflow | Core functionality. | Medium | Request, Approve, and Due Date tracking. |
| Returning Workflow | Core functionality. | Low | Record return and update availability. |
| Overdue Tracking | Critical for librarians. | Medium | Automated status changes or notifications. |
| Admin Dashboard | Management overview. | Medium | Stats on loans, overdue books, and requests. |

## Differentiators

Features that set product apart. Not expected, but valued.

| Feature | Value Proposition | Complexity | Notes |
|---------|-------------------|------------|-------|
| Reservation Queue | Allows users to wait for books. | High | Automatic notification when book returns. |
| Automatic Renewals | Convenience for students. | Medium | Renew if no active reservations exist. |
| Fine History | Transparency for fees. | Medium | Tracking unpaid vs paid late fees. |
| Dashboard Analytics | Deeper insights for librarians. | High | Visualizing borrowing trends over time. |

## Anti-Features

Features to explicitly NOT build (based on Project Spec).

| Anti-Feature | Why Avoid | What to Do Instead |
|--------------|-----------|-------------------|
| Online Fine Payment | Complexity/Security burden. | Log fine amount; pay at front desk. |
| E-book Delivery | Copyright/Format issues. | Focus on physical inventory management. |
| Inter-library Loans | Out of scope for Universitas XYZ. | Refer users to external university services. |
| Native Mobile App | High maintenance cost. | Build a responsive web app. |

## Feature Dependencies

```
User Authentication → Borrowing Workflow (Requires logged-in student)
Book Catalog → Borrowing Workflow (Requires book to select)
Borrowing Workflow → Returning Workflow (Requires active loan)
Returning Workflow → Late Fee Calculation (Requires return date comparison)
Borrowing Workflow → Admin Dashboard (Requires data to display)
```

## MVP Recommendation

Prioritize:
1. **Secure Authentication** (Role-based: Student/Librarian).
2. **Basic Catalog CRUD** (Add/Edit/Search Books).
3. **Core Lending Loop** (Borrow Request → Librarian Approval → Return).
4. **Basic Admin Dashboard** (List of active loans and overdue items).

Defer: **Reservation Queue** and **Fine Tracking** to Phase 2 once the core loop is stable.

## Sources

- [Universitas XYZ Project Spec](../../sample-project/library-management/PROJECT_SPEC.md)
- [Library Management Policy Research (WashU/Toledo)](https://washu.edu, https://toledolibrary.org)
