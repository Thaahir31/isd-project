from datetime import datetime

def calculate_overdue_fine(due_date: datetime, return_date: datetime) -> float:
    """
    Calculate fine: $0.50 per day overdue based on full 24-hour periods.
    Returns 0.0 if not overdue.
    """
    if return_date <= due_date:
        return 0.0
    
    delta = return_date - due_date
    days_overdue = delta.days
    
    # If return_date is on a later day than due_date but less than 24h difference,
    # delta.days will be 0. We'll stick to full 24h periods as per standard delta.days behavior.
    
    return float(max(0, days_overdue) * 0.50)
