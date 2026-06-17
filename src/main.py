from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from src.api import auth, authors, books, loans, members
from src.auth import require_role
from src.models.user import UserRole

app = FastAPI(title="Library Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(authors.router)
app.include_router(books.router)
app.include_router(loans.router)
app.include_router(members.router)


@app.get("/")
def serve_frontend():
    return FileResponse("templates/index.html")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/librarian-only", dependencies=[Depends(require_role(UserRole.LIBRARIAN))])
def librarian_only():
    return {"message": "Hello Librarian"}
