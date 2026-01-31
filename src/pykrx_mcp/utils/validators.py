"""Input validators for MCP tools."""


def validate_date_format(date_str: str) -> tuple[bool, str]:
    """
    Validate date string is in YYYYMMDD format.

    Only checks format, not validity (pykrx checks if date actually exists).

    Args:
        date_str: Date string to validate

    Returns:
        Tuple of (is_valid, error_message)
        - (True, "") if valid
        - (False, error_message) if invalid

    Examples:
        >>> validate_date_format("20240101")
        (True, "")
        >>> validate_date_format("2024-01-01")
        (False, "Date must be YYYYMMDD format (e.g., '20240101'), got: '2024-01-01'")
    """
    if not isinstance(date_str, str):
        return (
            False,
            f"Date must be a string, got {type(date_str).__name__}: {date_str}",
        )

    if len(date_str) != 8:
        msg = f"Date must be YYYYMMDD format (e.g., '20240101'), got: '{date_str}'"
        return False, msg

    if not date_str.isdigit():
        msg = f"Date must be YYYYMMDD format (e.g., '20240101'), got: '{date_str}'"
        return False, msg

    return True, ""


def validate_ticker_format(ticker: str) -> tuple[bool, str]:
    """
    Validate ticker is 6-digit Korean stock code.

    Only checks format, not existence (pykrx checks if ticker actually exists).

    Args:
        ticker: Stock ticker to validate

    Returns:
        Tuple of (is_valid, error_message)
        - (True, "") if valid
        - (False, error_message) if invalid

    Examples:
        >>> validate_ticker_format("005930")
        (True, "")
        >>> validate_ticker_format("5930")
        (False, "Ticker must be 6-digit string (e.g., '005930'), got: '5930'")
    """
    if not isinstance(ticker, str):
        return (
            False,
            f"Ticker must be a string, got {type(ticker).__name__}: {ticker}",
        )

    if len(ticker) != 6:
        msg = (
            f"Ticker must be 6-digit string "
            f"(e.g., '005930' for Samsung), got: '{ticker}'"
        )
        return False, msg

    if not ticker.isdigit():
        msg = f"Ticker must be 6-digit numeric string (e.g., '005930'), got: '{ticker}'"
        return False, msg

    return True, ""
