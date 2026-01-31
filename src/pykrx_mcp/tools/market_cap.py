"""Market capitalization tools."""

from pykrx import stock

from ..utils import (
    format_dataframe_response,
    format_error_response,
    mcp_tool_error_handler,
    validate_date_format,
    validate_ticker_format,
)


@mcp_tool_error_handler
def get_market_cap_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieve market capitalization data for a stock.

    Args:
        ticker: 6-digit stock ticker code (e.g., "005930" for Samsung Electronics)
        start_date: Start date in YYYYMMDD format (e.g., "20240101")
        end_date: End date in YYYYMMDD format (e.g., "20240131")

    Returns:
        Dictionary containing:
        - ticker: Stock ticker code
        - start_date: Query start date
        - end_date: Query end date
        - row_count: Number of data rows
        - data: List of dictionaries with market cap data
          (시가총액, 거래량, 거래대금, 상장주식수)
        - error: Error message if any (only present on error)

    Note:
        - Market cap (시가총액) is in Korean Won (KRW)
        - Trading volume (거래량) is number of shares traded
        - Trading value (거래대금) is in KRW
        - Outstanding shares (상장주식수) is total number of listed shares
    """
    # Validate ticker format
    valid, msg = validate_ticker_format(ticker)
    if not valid:
        return format_error_response(msg, ticker=ticker)

    # Validate start_date format
    valid, msg = validate_date_format(start_date)
    if not valid:
        return format_error_response(msg, date=start_date, field="start_date")

    # Validate end_date format
    valid, msg = validate_date_format(end_date)
    if not valid:
        return format_error_response(msg, date=end_date, field="end_date")

    # Fetch market cap data from pykrx
    df = stock.get_market_cap_by_date(
        fromdate=start_date, todate=end_date, ticker=ticker
    )

    if df.empty:
        return format_error_response(
            f"No market cap data found for ticker {ticker} "
            f"between {start_date} and {end_date}",
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

    return format_dataframe_response(
        df, ticker=ticker, start_date=start_date, end_date=end_date
    )
