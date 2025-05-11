
import isodate

def parse_duration(duration_str):
    """
    Converts ISO 8601 duration (e.g., 'PT15M30S') to seconds.
    """
    try:
        return isodate.parse_duration(duration_str).total_seconds()
    except Exception as e:
        print(f"Error parsing duration: {e}")
        return 0