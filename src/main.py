from fastapi import FastAPI, Depends
from src.api import auth, authors, books
from src.auth import require_role
from src.models.user import UserRole

app = FastAPI(title="Library Management System")

app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(books.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/librarian-only", dependencies=[Depends(require_role(UserRole.LIBRARIAN))])
def librarian_only():
    return {"message": "Hello Librarian"}
