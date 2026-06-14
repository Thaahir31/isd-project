from stdnum import isbn

def validate_isbn13(isbn_str: str) -> bool:
    """
    Validates if a string is a valid ISBN-13.
    Normalizes the input (removes dashes/spaces) before validation.
    """
    return isbn.is_valid(isbn_str) and len(isbn.compact(isbn_str)) == 13

def normalize_isbn(isbn_str: str) -> str:
    """
    Returns the compact version of the ISBN (no dashes or spaces).
    """
    return isbn.compact(isbn_str)
