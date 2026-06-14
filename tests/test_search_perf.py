import pytest
import time
from src.models.author import Author
from src.models.book import Book

def test_search_performance(client, db):
    # Seed books
    author = Author(name="Prolific Author")
    db.add(author)
    db.commit()

    def get_valid_isbn(i):
        # 978 + 9 digits + checksum
        base = f"978{i:09d}"
        total = 0
        for idx, char in enumerate(base):
            digit = int(char)
            if idx % 2 == 0:
                total += digit
            else:
                total += digit * 3
        checksum = (10 - (total % 10)) % 10
        return f"{base}{checksum}"

    books = [
        Book(
            title=f"Book Number {i}", 
            author_id=author.id, 
            isbn=get_valid_isbn(i), 
            total_copies=1
        ) for i in range(500)
    ]
    db.add_all(books)
    db.commit()

    start_time = time.time()
    response = client.get("/books/search?q=Number 50")
    end_time = time.time()

    duration = end_time - start_time
    assert response.status_code == 200
    assert len(response.json()) >= 1
    assert duration < 1.0, f"Search took too long: {duration}s"
    print(f"Search performance for 500 books: {duration:.4f}s")
