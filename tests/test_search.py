import pytest
from src.models.author import Author
from src.models.book import Book

@pytest.fixture
def seed_data(db):
    author1 = Author(name="Frank Herbert")
    author2 = Author(name="George Orwell")
    db.add_all([author1, author2])
    db.commit()

    book1 = Book(title="Dune", author_id=author1.id, isbn="9780441172719", category="Sci-Fi")
    book2 = Book(title="1984", author_id=author2.id, isbn="9780451524935", category="Dystopian")
    book3 = Book(title="Animal Farm", author_id=author2.id, isbn="9780452284241", category="Satire")
    db.add_all([book1, book2, book3])
    db.commit()
    return author1, author2

def test_search_by_title(client, seed_data):
    response = client.get("/books/search?q=Dune")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Dune"

def test_search_by_author(client, seed_data):
    response = client.get("/books/search?q=Orwell")
    assert response.status_code == 200
    assert len(response.json()) == 2
    titles = [b["title"] for b in response.json()]
    assert "1984" in titles
    assert "Animal Farm" in titles

def test_search_by_isbn(client, seed_data):
    response = client.get("/books/search?q=978-0-451-52493-5")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "1984"

def test_search_case_insensitive(client, seed_data):
    response = client.get("/books/search?q=dune")
    assert response.status_code == 200
    assert len(response.json()) == 1

def test_search_no_results(client, seed_data):
    response = client.get("/books/search?q=Unknown")
    assert response.status_code == 200
    assert len(response.json()) == 0
