"""Fundamental data related MCP tools."""

import logging

from pykrx import stock

from ..utils import (
    format_dataframe_response,
    format_error_response,
    mcp_tool_error_handler,
    validate_date_format,
    validate_ticker_format,
)

logger = logging.getLogger(__name__)


@mcp_tool_error_handler
def get_market_fundamental_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieve fundamental data (PER, PBR, dividend yield, etc.) for a stock.

    This tool fetches fundamental indicators that help evaluate stock valuation.
    Use this when you need to analyze a stock's fundamental metrics over time.

    Args:
        ticker: Stock ticker symbol (e.g., "005930" for Samsung Electronics)
        start_date: Start date in YYYYMMDD format (e.g., "20240101")
        end_date: End date in YYYYMMDD format (e.g., "20240131")

    Returns:
        Dictionary containing fundamental data including:
        - BPS (Book-value Per Share): 주당순자산가치
        - PER (Price Earnings Ratio): 주가수익비율
        - PBR (Price Book-value Ratio): 주가순자산비율
        - EPS (Earnings Per Share): 주당순이익
        - DIV (Dividend): 배당금
        - DPS (Dividend Per Share): 주당배당금

    Example:
        get_market_fundamental_by_date("005930", "20240101", "20240131")
        Returns Samsung Electronics fundamental data for January 2024
    """
    # Validate ticker format
    valid, msg = validate_ticker_format(ticker)
    if not valid:
        return format_error_response(msg, ticker=ticker)

    # Validate date formats
    valid, msg = validate_date_format(start_date)
    if not valid:
        return format_error_response(msg, start_date=start_date)

    valid, msg = validate_date_format(end_date)
    if not valid:
        return format_error_response(msg, end_date=end_date)

    # Fetch fundamental data
    df = stock.get_market_fundamental_by_date(
        fromdate=start_date, todate=end_date, ticker=ticker
    )

    # Check for empty results
    if df.empty:
        return format_error_response(
            f"No fundamental data found for ticker {ticker} in the date range",
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

    # Format successful response
    return format_dataframe_response(
        df, ticker=ticker, start_date=start_date, end_date=end_date
    )
