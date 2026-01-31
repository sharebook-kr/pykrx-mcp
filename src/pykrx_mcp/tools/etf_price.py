"""ETF related MCP tools."""

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
def get_etf_ohlcv_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieve ETF OHLCV (Open, High, Low, Close, Volume) data.

    This tool fetches historical ETF price data from the Korean market.
    Use this when you need to analyze ETF price movements or track performance.

    Args:
        ticker: ETF ticker symbol (e.g., "069500" for KODEX 200)
        start_date: Start date in YYYYMMDD format (e.g., "20240101")
        end_date: End date in YYYYMMDD format (e.g., "20240131")

    Returns:
        Dictionary containing ETF OHLCV data with dates as keys and
        price/volume information. Includes NAV (Net Asset Value) data.

    Example:
        get_etf_ohlcv_by_date("069500", "20240101", "20240131")
        Returns KODEX 200 ETF price data for January 2024
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

    # Fetch ETF OHLCV data
    df = stock.get_etf_ohlcv_by_date(
        fromdate=start_date, todate=end_date, ticker=ticker
    )

    # Check for empty results
    if df.empty:
        return format_error_response(
            f"No ETF data found for ticker {ticker} in the date range",
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

    # Format successful response
    return format_dataframe_response(
        df, ticker=ticker, start_date=start_date, end_date=end_date
    )


@mcp_tool_error_handler
def get_etf_ticker_list(date: str) -> dict:
    """
    Retrieve list of all ETF tickers traded on a specific date.

    Args:
        date: Date in YYYYMMDD format (e.g., "20240101")

    Returns:
        Dictionary with ETF ticker list and count

    Example:
        get_etf_ticker_list("20240101")
        Returns list of all ETFs traded on 2024-01-01
    """
    # Validate date format
    valid, msg = validate_date_format(date)
    if not valid:
        return format_error_response(msg, date=date)

    # Fetch ETF ticker list
    tickers = stock.get_etf_ticker_list(date)

    if len(tickers) == 0:
        return format_error_response(f"No ETFs found on {date}", date=date)

    # Convert to list if it's not already
    ticker_list = tickers.tolist() if hasattr(tickers, "tolist") else list(tickers)

    return {"date": date, "count": len(ticker_list), "tickers": ticker_list}
