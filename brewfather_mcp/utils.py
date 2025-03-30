from datetime import datetime


def convert_timestamp_to_iso8601(value: int | None):
    """Convert Unix timestamp to ISO 8601 formatted string."""
    if value is None:
        return None

    # If the value is an integer (Unix timestamp), convert it
    if isinstance(value, int):
        # Check if it's in milliseconds (13 digits) or seconds (10 digits)
        if len(str(value)) > 10:  # milliseconds
            timestamp_seconds = value / 1000
        else:  # seconds
            timestamp_seconds = value

        dt = datetime.fromtimestamp(timestamp_seconds)
        return dt.isoformat()

    return value
