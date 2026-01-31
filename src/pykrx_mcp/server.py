"""
pykrx-mcp: MCP server for Korean stock market data.

This module provides a FastMCP server that exposes pykrx functionality
to AI agents via the Model Context Protocol (MCP).
"""

import argparse
import logging
import os
import sys

from mcp.server.fastmcp import FastMCP

from .prompts import (
    analyze_investor_flow,
    analyze_stock_by_name,
    screen_undervalued_stocks,
)
from .resources import get_krx_info, get_pykrx_manual
from .tools import (
    get_etf_ohlcv_by_date as get_etf_ohlcv_impl,
)
from .tools import (
    get_etf_ticker_list as get_etf_ticker_list_impl,
)
from .tools import (
    get_market_cap_by_date as get_market_cap_impl,
)
from .tools import (
    get_market_fundamental_by_date as get_fundamental_impl,
)
from .tools import (
    get_market_ticker_list as get_ticker_list_impl,
)
from .tools import (
    get_market_ticker_name as get_ticker_name_impl,
)
from .tools import (
    get_market_trading_value_by_date as get_trading_value_impl,
)
from .tools import (
    get_stock_ohlcv as get_stock_ohlcv_impl,
)

# Configure logging to stderr BEFORE creating FastMCP instance
# (MCP uses stdout for protocol communication)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)

logger = logging.getLogger(__name__)

# Initialize FastMCP server
mcp = FastMCP("pykrx-mcp")


# ===== MCP Resources =====
# Resources provide static documentation that AI models can read


@mcp.resource("krx://info")
def _resource_krx_info() -> str:
    """General information about Korean stock market (KRX)."""
    return get_krx_info()


@mcp.resource("krx://pykrx-manual")
def _resource_pykrx_manual() -> str:
    """Comprehensive usage guide for pykrx MCP tools."""
    return get_pykrx_manual()


# ===== MCP Prompts =====
# Prompts provide pre-built workflows for common analysis tasks


@mcp.prompt()
def prompt_analyze_stock_by_name(
    stock_name: str, period: str = "1M", analysis_type: str = "price"
) -> str:
    """
    Analyze Korean stock by company name with automatic ticker lookup.

    Use this when users ask about stocks by their Korean company name
    instead of ticker codes. Handles the workflow of finding the ticker
    and then analyzing the stock data.

    Args:
        stock_name: Company name in Korean (e.g., "삼성전자", "네이버")
        period: Analysis period - "1W", "1M", "3M", "6M", "1Y" (default: "1M")
        analysis_type: Type of analysis - "price", "fundamental",
            "investor" (default: "price")

    Example:
        prompt_analyze_stock_by_name("삼성전자", "3M", "price")
    """
    return analyze_stock_by_name(stock_name, period, analysis_type)


@mcp.prompt()
def prompt_analyze_investor_flow(
    stock_name: str, period: str = "1M", focus_investor: str = "all"
) -> str:
    """
    Analyze investor trading patterns (foreign, institutional, individual).

    Provides step-by-step workflow to analyze supply/demand dynamics
    by different investor types and their correlation with stock price.

    Args:
        stock_name: Company name in Korean (e.g., "삼성전자")
        period: Analysis period - "1W", "1M", "3M", "6M", "1Y" (default: "1M")
        focus_investor: Focus on specific type - "foreign", "institution",
            "individual", "all" (default: "all")

    Example:
        prompt_analyze_investor_flow("삼성전자", "1M", "foreign")
    """
    return analyze_investor_flow(stock_name, period, focus_investor)


@mcp.prompt()
def prompt_screen_undervalued_stocks(
    max_per: float = 10.0,
    max_pbr: float = 1.0,
    market: str = "KOSPI",
    min_market_cap: int = 1000,
    sort_by: str = "PER",
) -> str:
    """
    Screen for potentially undervalued stocks based on fundamental metrics.

    Guides through multi-step workflow to find stocks with low PER/PBR,
    filter by market cap, and analyze the results.

    Args:
        max_per: Maximum PER threshold (default: 10.0)
        max_pbr: Maximum PBR threshold (default: 1.0)
        market: Target market - "KOSPI", "KOSDAQ", "ALL" (default: "KOSPI")
        min_market_cap: Minimum market cap in billions KRW (default: 1000)
        sort_by: Sort by - "PER", "PBR", "MarketCap", "EPS" (default: "PER")

    Example:
        prompt_screen_undervalued_stocks(max_per=10, max_pbr=1, market="KOSPI")
    """
    return screen_undervalued_stocks(max_per, max_pbr, market, min_market_cap, sort_by)


# ===== MCP Tools =====
# Tools are callable functions that AI models can invoke


@mcp.tool()
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
    return get_stock_ohlcv_impl(ticker, start_date, end_date, adjusted)


@mcp.tool()
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
    return get_ticker_list_impl(date, market)


@mcp.tool()
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
    return get_ticker_name_impl(ticker)


@mcp.tool()
def get_market_fundamental_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieve fundamental data (PER, PBR, dividend yield, etc.) for a stock.

    This tool fetches fundamental indicators that help evaluate stock valuation.

    Args:
        ticker: Stock ticker symbol (e.g., "005930" for Samsung Electronics)
        start_date: Start date in YYYYMMDD format (e.g., "20240101")
        end_date: End date in YYYYMMDD format (e.g., "20240131")

    Returns:
        Dictionary containing fundamental data (BPS, PER, PBR, EPS, DIV, DPS)

    Example:
        get_market_fundamental_by_date("005930", "20240101", "20240131")
        Returns Samsung fundamental data for January 2024
    """
    return get_fundamental_impl(ticker, start_date, end_date)


@mcp.tool()
def get_market_cap_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieve market capitalization data for a stock.

    Use this tool to get market cap, trading volume, trading value,
    and outstanding shares.

    Args:
        ticker: 6-digit stock ticker code (e.g., "005930" for Samsung Electronics)
        start_date: Start date in YYYYMMDD format (e.g., "20240101")
        end_date: End date in YYYYMMDD format (e.g., "20240131")

    Returns:
        Dictionary with market cap data including 시가총액, 거래량, 거래대금, 상장주식수
    """
    return get_market_cap_impl(ticker, start_date, end_date)


@mcp.tool()
def get_market_trading_value_by_date(
    ticker: str, start_date: str, end_date: str
) -> dict:
    """
    Retrieve trading value by investor type for supply/demand analysis.

    Essential for analyzing institutional and foreign investor flows.
    Positive values = net buying, negative values = net selling.

    Args:
        ticker: 6-digit stock ticker code (e.g., "005930" for Samsung Electronics)
        start_date: Start date in YYYYMMDD format (e.g., "20240101")
        end_date: End date in YYYYMMDD format (e.g., "20240131")

    Returns:
        Dictionary with trading value by investor type (금융투자, 외국인, 개인, etc.)
    """
    return get_trading_value_impl(ticker, start_date, end_date)


@mcp.tool()
def get_etf_ohlcv_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieve ETF OHLCV (Open, High, Low, Close, Volume) data.

    This tool fetches historical ETF price data from the Korean market.

    Args:
        ticker: ETF ticker symbol (e.g., "069500" for KODEX 200)
        start_date: Start date in YYYYMMDD format (e.g., "20240101")
        end_date: End date in YYYYMMDD format (e.g., "20240131")

    Returns:
        Dictionary containing ETF OHLCV data with NAV information

    Example:
        get_etf_ohlcv_by_date("069500", "20240101", "20240131")
        Returns KODEX 200 ETF price data for January 2024
    """
    return get_etf_ohlcv_impl(ticker, start_date, end_date)


@mcp.tool()
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
    return get_etf_ticker_list_impl(date)


def main():
    """Entry point for the MCP server."""
    parser = argparse.ArgumentParser(description="pykrx-mcp server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        help="Transport protocol: stdio for standard I/O (default), sse for HTTP/SSE",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "0.0.0.0"),
        help="Host to bind to for SSE transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "8000")),
        help="Port to bind to for SSE transport (default: 8000)",
    )

    args = parser.parse_args()

    if args.transport == "sse":
        logger.info(
            f"Starting pykrx-mcp server with SSE transport on {args.host}:{args.port}"
        )
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.info("Starting pykrx-mcp server with stdio transport")
        mcp.run()


if __name__ == "__main__":
    main()
