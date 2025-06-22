from datetime import datetime


def parse_iso_datetime(iso_string, output_format="%d-%m-%Y %H:%M"):
    """Parse ISO datetime string to formatted string."""
    try:
        dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ")
        return dt.strftime(output_format)
    except (ValueError, TypeError):
        return iso_string
