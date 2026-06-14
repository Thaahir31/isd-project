# Architecture Patterns

**Domain:** Library Management System
**Researched:** 2026-12-06

## Recommended Architecture

The system follows a standard **Layered Architecture** with a FastAPI backend and a PostgreSQL database.

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| **API Layer (FastAPI)** | Handling HTTP requests, routing, validation. | Service Layer |
| **Service Layer** | Business logic (borrowing rules, fine calculation). | Repository Layer |
| **Repository Layer (SQLAlchemy)** | Database abstractions and queries. | PostgreSQL |
| **Auth Provider** | JWT token generation and user verification. | Service Layer |

### Data Flow

1. **Request:** Student searches for a book via `GET /books?title=...`.
2. **Logic:** API validates query → Service layer calls Repository → Repository queries PostgreSQL.
3. **Response:** Book list returned as JSON.
4. **Action:** Student requests book `POST /loans/request`.
5. **Logic:** System checks availability → Creates `Loan` record with `PENDING` status.

## Patterns to Follow

### Pattern 1: Role-Based Access Control (RBAC)
**What:** Restricting endpoints based on user roles (Student vs. Librarian).
**When:** All sensitive operations (CRUD books, approve loans).
**Example:**
```python
@app.post("/books", dependencies=[Depends(get_current_active_librarian)])
def add_book(book: BookCreate):
    return crud.create_book(book)
```

### Pattern 2: State Machine for Loans
**What:** Defining clear states for a book loan.
**States:** `REQUESTED` → `ACTIVE` → `RETURNED` (or `OVERDUE` → `RETURNED`).
**Instead of:** Using multiple boolean flags.

## Recommended Data Model (Entities)

| Entity | Attributes |
|--------|------------|
| **User** | id, email, hashed_password, role (student/librarian), is_active |
| **Book** | id, title, isbn, summary, total_copies, available_copies |
| **Author** | id, name, biography |
| **Loan** | id, user_id, book_id, borrow_date, due_date, return_date, status |
| **Fine** | id, loan_id, amount, status (paid/unpaid) |

## API Endpoint Mapping (Draft)

| Method | Endpoint | Description | Auth Role |
|--------|----------|-------------|-----------|
| GET | `/books` | Search catalog | Any |
| POST | `/books` | Add new book | Librarian |
| POST | `/loans/request` | Request a book | Student |
| POST | `/loans/{id}/approve` | Approve request | Librarian |
| POST | `/loans/{id}/return` | Record return | Librarian |

## Scalability Considerations

| Concern | At 100 users | At 10K users | At 1M users |
|---------|--------------|--------------|-------------|
| Database | Single SQLite/Postgres | Optimized Postgres (Indices) | Read Replicas / Sharding |
| Search | SQL `LIKE` | Postgres Full-Text Search | Elasticsearch / Meilisearch |
| Auth | Memory/Simple JWT | Redis for Token Blacklisting | Dedicated Auth Service |

## Sources

- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [Database Design for LMS (Standard Patterns)](https://github.com/Shraddha-Shetty/Developing-api-with-python)
