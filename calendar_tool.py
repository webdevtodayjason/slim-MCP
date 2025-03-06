import datetime
import calendar

def get_month_calendar(year=None, month=None):
    """
    Get a calendar for the specified month.
    
    Args:
        year (int, optional): Year. Defaults to current year.
        month (int, optional): Month (1-12). Defaults to current month.
    
    Returns:
        dict: Month calendar information
    """
    if year is None:
        year = datetime.datetime.now().year
    if month is None:
        month = datetime.datetime.now().month
    
    try:
        # Get month name
        month_name = calendar.month_name[month]
        
        # Get calendar matrix
        cal = calendar.monthcalendar(year, month)
        
        # Get days of the week
        days_of_week = list(calendar.day_name)
        
        result = {
            "year": year,
            "month": month,
            "month_name": month_name,
            "days_of_week": days_of_week,
            "calendar": cal
        }
        
        return result
    except Exception as e:
        return {"error": f"Error generating calendar: {str(e)}"}

def get_upcoming_dates(date_type, count=5):
    """
    Get upcoming dates of a specific type.
    
    Args:
        date_type (str): Type of dates to retrieve (holidays, weekends, etc.)
        count (int, optional): Number of dates to retrieve. Defaults to 5.
    
    Returns:
        dict: Upcoming dates information
    """
    today = datetime.date.today()
    
    if date_type.lower() == "weekend":
        # Find upcoming weekends
        upcoming = []
        current_date = today
        
        while len(upcoming) < count:
            current_date += datetime.timedelta(days=1)
            if current_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                upcoming.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": calendar.day_name[current_date.weekday()]
                })
        
        return {"upcoming_weekends": upcoming}
    
    elif date_type.lower() == "business_days":
        # Find upcoming business days
        upcoming = []
        current_date = today
        
        while len(upcoming) < count:
            current_date += datetime.timedelta(days=1)
            if current_date.weekday() < 5:  # 0-4 = Monday-Friday
                upcoming.append({
                    "date": current_date.strftime("%Y-%m-%d"),
                    "day": calendar.day_name[current_date.weekday()]
                })
        
        return {"upcoming_business_days": upcoming}
    
    else:
        return {"error": "Unsupported date type. Supported types: weekend, business_days"}