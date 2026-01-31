"""Stock price related MCP tools."""

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
def get_stock_ohlcv(
    ticker: str, start_date: str, end_date: str, adjusted: bool = True
) -> dict:
    """
    Retrieve OHLCV (Open, High, Low, Close, Volume) data for a Korean stock.

    This tool fetches historical stock price data from the Korean stock
    market (KRX). Use this when you need to analyze stock price movements,
    calculate technical indicators, or visualize price trends for Korean
    stocks.

    Args:
        ticker: Stock ticker symbol (e.g., "005930" for Samsung Electronics).
                Korean stock tickers are 6-digit numbers.
        start_date: Start date in YYYYMMDD format (e.g., "20240101").
        end_date: End date in YYYYMMDD format (e.g., "20240131").
        adjusted: Whether to return adjusted prices (default: True).
                  Adjusted prices account for stock splits and dividends.

    Returns:
        Dictionary containing OHLCV data with dates as keys and price/volume
        information. Each entry includes: Open, High, Low, Close, Volume, and
        trading value.

    Example:
        get_stock_ohlcv("005930", "20240101", "20240131", True)
        Returns Samsung Electronics stock data for January 2024.
    """
    # Validate input formats (MCP layer responsibility)
    valid, msg = validate_ticker_format(ticker)
    if not valid:
        return format_error_response(msg, ticker=ticker)

    valid, msg = validate_date_format(start_date)
    if not valid:
        return format_error_response(msg, start_date=start_date)

    valid, msg = validate_date_format(end_date)
    if not valid:
        return format_error_response(msg, end_date=end_date)

    # Fetch data from pykrx (domain logic)
    df = stock.get_market_ohlcv_by_date(
        fromdate=start_date, todate=end_date, ticker=ticker, adjusted=adjusted
    )

    # Check for empty results
    if df.empty:
        return format_error_response(
            f"No data found for ticker {ticker} in the specified date range",
            ticker=ticker,
            start_date=start_date,
            end_date=end_date,
        )

    # Format successful response
    return format_dataframe_response(
        df,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        adjusted=adjusted,
    )
