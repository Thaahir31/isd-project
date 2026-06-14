# Technology Stack

**Project:** Library Management System
**Researched:** 2026-12-06

## Recommended Stack

### Core Framework
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | 3.11+ | Backend Language | Standard for modern backend dev; great library support. |
| FastAPI | Latest | API Framework | High performance, async support, automatic OpenAPI docs. |
| PostgreSQL | 15+ | Database | Reliable relational database for complex joins (Books, Loans, Users). |
| SQLAlchemy | 2.0+ | ORM | Database abstraction with strong typing and async support. |

### Infrastructure
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Docker | Latest | Containerization | Ensures consistent environments across dev and deployment. |
| Docker Compose | Latest | Orchestration | Simplifies running multi-container apps (API + DB). |

### Supporting Libraries
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Pydantic | 2.0+ | Data Validation | Request/Response schema validation. |
| Alembic | Latest | DB Migrations | Managing database schema changes over time. |
| PyJWT | Latest | Authentication | JWT token generation and verification. |
| Passlib | Latest | Password Hashing | Securely hashing user passwords (using bcrypt). |
| pytest | Latest | Testing | Unit and integration testing. |

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| API Framework | FastAPI | Django | Django is more "batteries-included" but heavier. FastAPI is more performant and better for pure APIs. |
| Database | PostgreSQL | SQLite | SQLite is good for small projects, but PostgreSQL is better for multi-user university systems. |

## Installation

```bash
# Core
pip install fastapi[all] sqlalchemy psycopg2-binary passlib[bcrypt] python-jose[cryptography]

# Dev dependencies
pip install pytest alembic black isort
```

## Sources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/)
- [GitHub: tannmayyy/library-management-system](https://github.com/tannmayyy/library-management-system)
- [GitHub: Rohanpudasaini/library_management_system_fastAPI](https://github.com/Rohanpudasaini/library_management_system_fastAPI)
