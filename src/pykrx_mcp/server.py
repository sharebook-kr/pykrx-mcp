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
    get_exhaustion_rates_of_foreign_investment as get_foreign_investment_impl,
)
from .tools import (
    get_index_fundamental as get_index_fundamental_impl,
)
from .tools import (
    get_index_ohlcv as get_index_ohlcv_impl,
)
from .tools import (
    get_index_portfolio_deposit_file as get_index_portfolio_impl,
)
from .tools import (
    get_index_ticker_list as get_index_ticker_list_impl,
)
from .tools import (
    get_index_ticker_name as get_index_ticker_name_impl,
)
from .tools import (
    get_market_cap_by_date as get_market_cap_impl,
)
from .tools import (
    get_market_fundamental_by_date as get_fundamental_impl,
)
from .tools import (
    get_market_net_purchases_of_equities as get_net_purchases_impl,
)
from .tools import (
    get_market_ohlcv_by_date as get_market_ohlcv_impl,
)
from .tools import (
    get_market_price_change as get_price_change_impl,
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
    get_market_trading_value_by_investor as get_trading_value_investor_impl,
)
from .tools import (
    get_market_trading_volume_by_investor as get_trading_volume_investor_impl,
)
from .tools import (
    get_shorting_balance_top50 as get_shorting_balance_top50_impl,
)
from .tools import (
    get_shorting_status_by_date as get_shorting_status_impl,
)
from .tools import (
    get_shorting_volume_by_ticker as get_shorting_volume_impl,
)
from .tools import (
    get_shorting_volume_top50 as get_shorting_volume_top50_impl,
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


# ===== Index Tools =====


@mcp.tool()
def get_index_ticker_list(date: str = None, market: str = "KOSPI") -> dict:
    """
    Get list of index tickers (KOSPI/KOSDAQ indices).

    Args:
        date: Date in YYYYMMDD format, omit for latest (e.g., "20240101")
        market: Market type - KOSPI or KOSDAQ (default: KOSPI)

    Returns:
        Dictionary with index ticker list

    Example:
        get_index_ticker_list("20240101", "KOSPI")
    """
    return get_index_ticker_list_impl(date, market)


@mcp.tool()
def get_index_ticker_name(ticker: str) -> dict:
    """
    Get the name of an index from its ticker.

    Args:
        ticker: Index ticker (e.g., "1001" for KOSPI)

    Returns:
        Dictionary with ticker and index name

    Example:
        get_index_ticker_name("1001")
    """
    return get_index_ticker_name_impl(ticker)


@mcp.tool()
def get_index_ohlcv(
    ticker: str, start_date: str, end_date: str, freq: str = "d"
) -> dict:
    """
    Get index OHLCV data.

    Args:
        ticker: Index ticker (e.g., "1001" for KOSPI)
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        freq: Frequency - d (daily), m (monthly), y (yearly)

    Returns:
        Dictionary with index OHLCV data

    Example:
        get_index_ohlcv("1001", "20240101", "20240131", "d")
    """
    return get_index_ohlcv_impl(ticker, start_date, end_date, freq)


@mcp.tool()
def get_index_fundamental(
    start_date: str, end_date: str = None, ticker: str = None
) -> dict:
    """
    Get index fundamental data (PER/PBR/dividend yield).

    Args:
        start_date: Start date in YYYYMMDD format
        end_date: End date (optional, for specific index over time)
        ticker: Index ticker (optional, for specific index)

    Returns:
        Dictionary with fundamental indicators

    Example:
        get_index_fundamental("20240101", "20240131", "1001")
    """
    return get_index_fundamental_impl(start_date, end_date, ticker)


@mcp.tool()
def get_index_portfolio_deposit_file(ticker: str, date: str = None) -> dict:
    """
    Get constituent stocks of an index.

    Args:
        ticker: Index ticker (e.g., "1005" for textile/clothing)
        date: Date in YYYYMMDD format (optional, defaults to latest)

    Returns:
        Dictionary with constituent ticker list

    Example:
        get_index_portfolio_deposit_file("1005")
    """
    return get_index_portfolio_impl(ticker, date)


# ===== Short Selling Tools =====


@mcp.tool()
def get_shorting_status_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Get short selling status for a stock.

    Args:
        ticker: 6-digit stock ticker
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format

    Returns:
        Dictionary with short selling volume and balance data

    Example:
        get_shorting_status_by_date("005930", "20240101", "20240131")
    """
    return get_shorting_status_impl(ticker, start_date, end_date)


@mcp.tool()
def get_shorting_volume_by_ticker(date: str, market: str = "KOSPI") -> dict:
    """
    Get short selling volume for all stocks on a date.

    Args:
        date: Date in YYYYMMDD format
        market: Market type - KOSPI/KOSDAQ/KONEX

    Returns:
        Dictionary with short selling volume by ticker

    Example:
        get_shorting_volume_by_ticker("20240101", "KOSPI")
    """
    return get_shorting_volume_impl(date, market)


@mcp.tool()
def get_shorting_balance_top50(date: str, market: str = "KOSPI") -> dict:
    """
    Get top 50 stocks by short selling balance ratio.

    Args:
        date: Date in YYYYMMDD format
        market: Market type - KOSPI or KOSDAQ

    Returns:
        Dictionary with top 50 stocks ranked by short balance

    Example:
        get_shorting_balance_top50("20240101", "KOSPI")
    """
    return get_shorting_balance_top50_impl(date, market)


@mcp.tool()
def get_shorting_volume_top50(date: str, market: str = "KOSPI") -> dict:
    """
    Get top 50 stocks by short selling trading ratio.

    Args:
        date: Date in YYYYMMDD format
        market: Market type - KOSPI or KOSDAQ

    Returns:
        Dictionary with top 50 stocks ranked by short volume

    Example:
        get_shorting_volume_top50("20240101", "KOSPI")
    """
    return get_shorting_volume_top50_impl(date, market)


# ===== Investor Trading Tools =====


@mcp.tool()
def get_market_trading_volume_by_investor(
    start_date: str, end_date: str, ticker: str
) -> dict:
    """
    Get net purchase volume by investor type.

    Args:
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        ticker: Stock ticker or market (KOSPI/KOSDAQ/KONEX/ALL)

    Returns:
        Dictionary with investor trading volume (buy/sell/net)

    Example:
        get_market_trading_volume_by_investor("20240101", "20240131", "005930")
    """
    return get_trading_volume_investor_impl(start_date, end_date, ticker)


@mcp.tool()
def get_market_trading_value_by_investor(
    start_date: str, end_date: str, ticker: str
) -> dict:
    """
    Get net purchase value by investor type.

    Args:
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        ticker: Stock ticker or market (KOSPI/KOSDAQ/KONEX/ALL)

    Returns:
        Dictionary with investor trading value (buy/sell/net)

    Example:
        get_market_trading_value_by_investor("20240101", "20240131", "KOSPI")
    """
    return get_trading_value_investor_impl(start_date, end_date, ticker)


@mcp.tool()
def get_market_net_purchases_of_equities(
    start_date: str, end_date: str, market: str, investor: str
) -> dict:
    """
    Get top stocks by net purchases for specific investor type.

    Args:
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        market: Market type (KOSPI/KOSDAQ/KONEX/ALL)
        investor: Investor type (금융투자/보험/투신/사모/은행/기관합계/개인/외국인 etc.)

    Returns:
        Dictionary with top stocks ranked by net purchases

    Example:
        get_market_net_purchases_of_equities("20240101", "20240131", "KOSPI", "외국인")
    """
    return get_net_purchases_impl(start_date, end_date, market, investor)


# ===== Foreign Investment Tools =====


@mcp.tool()
def get_exhaustion_rates_of_foreign_investment(
    start_date: str,
    end_date: str = None,
    ticker: str = None,
    market: str = "KOSPI",
    balance_limit: bool = False,
) -> dict:
    """
    Get foreign ownership and investment limit exhaustion rates.

    Args:
        start_date: Start date in YYYYMMDD format
        end_date: End date (optional, for specific stock over time)
        ticker: Stock ticker (optional, for specific stock)
        market: Market type - KOSPI/KOSDAQ/KONEX
        balance_limit: Only show stocks with foreign ownership limits

    Returns:
        Dictionary with foreign ownership data

    Example:
        get_exhaustion_rates_of_foreign_investment("20240101", market="KOSPI")
    """
    return get_foreign_investment_impl(
        start_date, end_date, ticker, market, balance_limit
    )


# ===== Market-wide Data Tools =====


@mcp.tool()
def get_market_ohlcv_by_date(date: str, market: str = "KOSPI") -> dict:
    """
    Get OHLCV for all stocks on a specific date.

    Args:
        date: Date in YYYYMMDD format
        market: Market type - KOSPI/KOSDAQ/KONEX/ALL

    Returns:
        Dictionary with OHLCV data for all stocks

    Example:
        get_market_ohlcv_by_date("20240101", "KOSPI")
    """
    return get_market_ohlcv_impl(date, market)


@mcp.tool()
def get_market_price_change(
    start_date: str, end_date: str, market: str = "KOSPI"
) -> dict:
    """
    Get price change for all stocks over a period.

    Args:
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format
        market: Market type - KOSPI/KOSDAQ/KONEX/ALL

    Returns:
        Dictionary with price changes for all stocks

    Example:
        get_market_price_change("20240101", "20240131", "KOSPI")
    """
    return get_price_change_impl(start_date, end_date, market)


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
