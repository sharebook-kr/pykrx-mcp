"""Trading value tools for supply and demand analysis."""

from pykrx import stock

from ..utils import (
    format_dataframe_response,
    format_error_response,
    mcp_tool_error_handler,
    validate_date_format,
    validate_ticker_format,
)


@mcp_tool_error_handler
def get_market_trading_value_by_date(
    ticker: str, start_date: str, end_date: str
) -> dict:
    """
    Retrieve trading value by investor type for supply/demand analysis.

    This tool is essential for analyzing institutional and foreign investor flows,
    which are key indicators for supply and demand dynamics in Korean markets.

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
        - data: List of dictionaries with trading value by investor type
          (금융투자, 보험, 투신, 사모, 은행, 기타금융, 연기금등, 기타법인,
          개인, 외국인, 기타외국인)
        - error: Error message if any (only present on error)

    Note:
        - All values are in Korean Won (KRW)
        - Positive values indicate net buying, negative values indicate net selling
        - Key investor types:
          * 금융투자: Securities firms
          * 외국인: Foreign investors
          * 기관: Institutional investors (sum of 금융투자, 보험, 투신, etc.)
          * 개인: Individual investors
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

    # Fetch trading value data from pykrx
    df = stock.get_market_trading_value_by_date(
        fromdate=start_date, todate=end_date, ticker=ticker
    )

    if df.empty:
        return format_error_response(
            f"No trading value data found for ticker {ticker} "
            f"between {start_date} and {end_date}",
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

    return format_dataframe_response(
        df, ticker=ticker, start_date=start_date, end_date=end_date
    )
