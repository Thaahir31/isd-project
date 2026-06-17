from datetime import datetime, timedelta
from src.logic.fines import calculate_overdue_fine

def test_fine_on_time():
    due_date = datetime(2023, 1, 1, 12, 0)
    return_date = datetime(2023, 1, 1, 11, 0)
    assert calculate_overdue_fine(due_date, return_date) == 0.0

def test_fine_same_time():
    due_date = datetime(2023, 1, 1, 12, 0)
    return_date = datetime(2023, 1, 1, 12, 0)
    assert calculate_overdue_fine(due_date, return_date) == 0.0

def test_fine_one_day_late():
    due_date = datetime(2023, 1, 1, 12, 0)
    return_date = datetime(2023, 1, 2, 12, 0)
    assert calculate_overdue_fine(due_date, return_date) == 0.50

def test_fine_ten_days_late():
    due_date = datetime(2023, 1, 1, 12, 0)
    return_date = datetime(2023, 1, 11, 13, 0)
    assert calculate_overdue_fine(due_date, return_date) == 5.0

def test_fine_less_than_24h_late():
    due_date = datetime(2023, 1, 1, 12, 0)
    return_date = datetime(2023, 1, 2, 11, 0)
    # delta.days is 0 because it's only 23 hours
    assert calculate_overdue_fine(due_date, return_date) == 0.0
