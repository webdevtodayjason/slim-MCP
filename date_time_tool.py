import datetime

def get_current_datetime():
    """Get the current date and time information."""
    now = datetime.datetime.now()
    result = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
        "timestamp": now.timestamp(),
        "timezone": datetime.datetime.now().astimezone().tzname(),
        "iso_format": now.isoformat()
    }
    return result

def format_date(date_str, format_str):
    """Format a date string according to specified format."""
    try:
        # First try parsing as ISO format
        date_obj = datetime.datetime.fromisoformat(date_str)
    except ValueError:
        try:
            # Then try common format YYYY-MM-DD
            date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            return {"error": "Invalid date format. Please use ISO format or YYYY-MM-DD"}
    
    try:
        formatted_date = date_obj.strftime(format_str)
        return {"formatted_date": formatted_date}
    except ValueError:
        return {"error": "Invalid format string"}