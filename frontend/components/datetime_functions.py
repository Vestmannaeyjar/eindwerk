from datetime import datetime


def parse_iso_datetime(iso_string, output_format="%d-%m-%Y %H:%M"):
    """Parse ISO datetime string to formatted string."""
    try:
        # First try with +00:00 format (what your system is sending)
        dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S+00:00")
        return dt.strftime(output_format)
    except ValueError:
        try:
            # Fallback to Z format
            dt = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%SZ")
            return dt.strftime(output_format)
        except ValueError:
            try:
                # Try with fromisoformat which handles both formats automatically
                dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
                return dt.strftime(output_format)
            except (ValueError, TypeError):
                return iso_string


def parse_date(date_string):
    """Parse date string in dd-mm-yyyy or dd-mm-yyyy hh:mm format."""
    if not date_string or not date_string.strip():
        return None

    date_string = date_string.strip()

    # Try different formats
    formats = [
        "%d-%m-%Y %H:%M",  # dd-mm-yyyy hh:mm
        "%d-%m-%Y",  # dd-mm-yyyy
        "%Y-%m-%dT%H:%M:%S+00:00",  # ISO format with +00:00 (what system sends)
        "%Y-%m-%dT%H:%M:%SZ",  # ISO format with Z
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_string, fmt)
            # Return in ISO format for API (using Z format as requested)
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        except ValueError:
            continue

    raise ValueError("Ongeldige datum/tijd formaat. Gebruik dd-mm-jjjj hh:mm")