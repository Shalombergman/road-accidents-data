from datetime import datetime, timedelta

from repository.accidents_repository import get_accidents_by_region_and_date


def get_accidents_by_period(region, start_date_str, period_type):

    start_date = parse_date(start_date_str)

    if period_type == "day":
        end_date = start_date + timedelta(days=1)
    elif period_type == "week":
        end_date = start_date + timedelta(weeks=1)
    elif period_type == "month":
        if start_date.month == 12:
            end_date = datetime(start_date.year + 1, 1, start_date.day)
        else:
            end_date = datetime(start_date.year, start_date.month + 1, start_date.day)
    else:
        raise ValueError("Invalid period type. Use 'day', 'week', or 'month'.")

    return get_accidents_by_region_and_date(region, start_date, end_date)
from datetime import datetime



def parse_date(date_str):
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    raise ValueError(f"Date format not recognized for: {date_str}")
