"""Ticker information related MCP tools."""

import logging

from pykrx import stock

from ..utils import (
    format_error_response,
    mcp_tool_error_handler,
    validate_date_format,
    validate_ticker_format,
)

logger = logging.getLogger(__name__)


@mcp_tool_error_handler
def get_market_ticker_list(date: str, market: str = "KOSPI") -> dict:
    """
    Retrieve list of stock tickers for a specific market.

    Args:
        date: Date in YYYYMMDD format (e.g., "20240101")
        market: Market name - "KOSPI", "KOSDAQ", or "KONEX" (default: "KOSPI")

    Returns:
        Dictionary with ticker list and count

    Example:
        get_market_ticker_list("20240101", "KOSPI")
        Returns list of all KOSPI stocks on 2024-01-01
    """
    # Validate date format
    valid, msg = validate_date_format(date)
    if not valid:
        return format_error_response(msg, date=date, market=market)

    # Validate market
    valid_markets = ["KOSPI", "KOSDAQ", "KONEX"]
    if market not in valid_markets:
        return format_error_response(
            f"Market must be one of {valid_markets}, got: '{market}'",
            date=date,
            market=market,
        )

    # Fetch ticker list
    tickers = stock.get_market_ticker_list(date, market=market)

    if len(tickers) == 0:
        return format_error_response(
            f"No tickers found for {market} on {date}",
            date=date,
            market=market,
        )

    # Convert to list if it's not already
    ticker_list = tickers.tolist() if hasattr(tickers, "tolist") else list(tickers)

    return {
        "date": date,
        "market": market,
        "count": len(ticker_list),
        "tickers": ticker_list,
    }


@mcp_tool_error_handler
def get_market_ticker_name(ticker: str) -> dict:
    """
    Get the name of a stock from its ticker code.

    Args:
        ticker: 6-digit stock ticker code (e.g., "005930")

    Returns:
        Dictionary with ticker and company name

    Example:
        get_market_ticker_name("005930")
        Returns {"ticker": "005930", "name": "삼성전자"}
    """
    # Validate ticker format
    valid, msg = validate_ticker_format(ticker)
    if not valid:
        return format_error_response(msg, ticker=ticker)

    # Fetch ticker name
    name = stock.get_market_ticker_name(ticker)

    if not name or name == "":
        return format_error_response(
            f"Ticker {ticker} not found or delisted", ticker=ticker
        )

    return {"ticker": ticker, "name": name}
