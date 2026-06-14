from src.logic.isbn import validate_isbn13

def test_valid_isbn13():
    assert validate_isbn13("978-3-16-148410-0") is True
    assert validate_isbn13("9783161484100") is True

def test_invalid_isbn13():
    assert validate_isbn13("1234567890") is False
    assert validate_isbn13("978-3-16-148410-1") is False  # Wrong checksum

def test_isbn10_is_rejected():
    # Even if valid ISBN-10, we strictly want ISBN-13 per context
    assert validate_isbn13("0-306-40615-2") is False
