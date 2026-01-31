import logging
import sys

from mcp.server.fastmcp import FastMCP
from pykrx import stock

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


# Add a simple resource for testing
@mcp.resource("krx://info")
def get_krx_info() -> str:
    """General information about Korean stock market (KRX)."""
    return """
    # Korean Stock Exchange (KRX) Information

    The Korea Exchange (KRX) operates:
    - KOSPI: Korea Composite Stock Price Index (main board)
    - KOSDAQ: Korean Securities Dealers Automated Quotations (tech/growth stocks)

    Trading hours: 09:00-15:30 KST (Mon-Fri)
    Stock tickers: 6-digit codes (e.g., 005930 for Samsung Electronics)
    """


@mcp.resource("krx://pykrx-manual")
def get_pykrx_manual() -> str:
    """Comprehensive usage guide for pykrx MCP tools."""
    return """
    # Pykrx Tool Usage Guide

    This MCP server provides access to Korean stock market data via the `pykrx` library.
    Read this guide carefully to use the tools correctly and efficiently.

    ## 1. Data Format & Constraints

    ### Date Format
    - **REQUIRED FORMAT:** `YYYYMMDD` (8-digit string)
    - ✅ Correct: "20240101", "20231215"
    - ❌ Wrong: "2024-01-01", "01/01/2024", "20240101T00:00:00"

    ### Ticker Format
    - **6-digit string codes** (with leading zeros)
    - ✅ Correct: "005930" (Samsung Electronics), "000660" (SK Hynix)
    - ❌ Wrong: "5930", "SSNLF" (US tickers won't work)

    ### Supported Markets
    - **KOSPI:** Main board (large cap stocks)
    - **KOSDAQ:** Technology and growth stocks
    - **KONEX:** Small & medium enterprise market

    ### Data Availability
    - Historical data generally available from **1990** onwards for KOSPI
    - KOSDAQ data typically starts from mid-1990s
    - Very recent data may have 1-day lag
    - **No real-time data:** All data is end-of-day (EOD)

    ## 2. Tool Selection Guide

    Choose the right tool based on the user's question:

    ### Stock Price Analysis
    - **Question:** "Show me Samsung's stock price last month"
    - **Tool:** `get_stock_ohlcv`
    - **Why:** Provides Open, High, Low, Close, Volume data

    ### Finding Ticker Codes
    - **Question:** "What's the ticker for Samsung Electronics?"
    - **Approach:** Korean stock tickers are numeric. Major stocks:
      - Samsung Electronics: 005930
      - SK Hynix: 000660
      - Naver: 035420
      - Kakao: 035720
    - **Future tool:** `get_ticker_by_name` (not yet implemented)

    ### Market-wide Analysis
    - **Question:** "List all KOSPI stocks"
    - **Future tool:** `get_market_ticker_list` (not yet implemented)

    ### Investor Trading Patterns
    - **Question:** "Show foreign investor buying/selling for Samsung"
    - **Future tool:** `get_market_net_purchases_of_equities_by_ticker`

    ## 3. Best Practices

    ### For Long-term Analysis
    - **DON'T:** Request 10+ years of daily data in one call
    - **DO:** Fetch data in chunks (1-2 years at a time)
    - **Reason:** Prevents timeout and reduces server load

    ### For Multiple Stocks
    - **DON'T:** Make 100+ sequential requests without delay
    - **DO:** Batch requests and add small delays between calls
    - **Reason:** KRX server may rate-limit excessive requests

    ### When Data is Missing
    - Empty results usually mean:
      1. Ticker doesn't exist or is delisted
      2. Date range is outside trading history
      3. Date falls on weekend/holiday (markets closed)
    - **Action:** Verify ticker code and date range, check if trading day

    ## 4. Error Handling

    ### Common Error Patterns

    **"No data found for ticker"**
    - Verify 6-digit ticker format (include leading zeros)
    - Check if stock was trading during requested period
    - Confirm date is not a holiday/weekend

    **Empty DataFrame returned**
    - Date range may be outside available history
    - Market might have been closed (holidays)
    - Try expanding date range or checking market calendar

    **Rate limiting (HTTP 429 or timeout)**
    - You're requesting data too quickly
    - Add delays between requests (1-2 seconds)
    - Reduce the scope of your query

    ## 5. Performance Tips

    - **Adjusted vs. Unadjusted prices:**
      - Use `adjusted=True` for accurate long-term analysis
      - Accounts for stock splits and dividends
      - Default is `True` for most tools

    - **Date range optimization:**
      - Shorter ranges = faster responses
      - For backtesting, consider monthly/weekly data instead of daily

    ## 6. Known Limitations

    - **No intraday data:** Only daily OHLCV available
    - **T+1 delay:** Today's data usually available next day
    - **No options/futures:** Only equity (stock) data
    - **Korean market only:** No access to US, EU, or other markets
    - **Historical limit:** Some stocks have limited history before IPO

    ## 7. Quick Reference Examples

    ```
    # Samsung Electronics daily prices for Jan 2024
    get_stock_ohlcv("005930", "20240101", "20240131", adjusted=True)

    # SK Hynix weekly analysis (use start of each week)
    get_stock_ohlcv("000660", "20230101", "20231231", adjusted=True)
    ```

    **Remember:** Always validate date formats and ticker codes before calling tools.
    When errors occur, refer back to this guide for troubleshooting steps.
    """


@mcp.tool()
def get_stock_ohlcv(
    ticker: str, start_date: str, end_date: str, adjusted: bool = True
) -> dict:
    """
    Retrieve OHLCV (Open, High, Low, Close, Volume) data for a Korean stock.

    This tool fetches historical stock price data from the Korean stock market (KRX).
    Use this when you need to analyze stock price movements, calculate technical indicators,
    or visualize price trends for Korean stocks.

    Args:
        ticker: Stock ticker symbol (e.g., "005930" for Samsung Electronics).
                Korean stock tickers are 6-digit numbers.
        start_date: Start date in YYYYMMDD format (e.g., "20240101").
        end_date: End date in YYYYMMDD format (e.g., "20240131").
        adjusted: Whether to return adjusted prices (default: True).
                  Adjusted prices account for stock splits and dividends.

    Returns:
        Dictionary containing OHLCV data with dates as keys and price/volume information.
        Each entry includes: Open, High, Low, Close, Volume, and trading value.

    Example:
        get_stock_ohlcv("005930", "20240101", "20240131", True)
        Returns Samsung Electronics stock data for January 2024.
    """
    try:
        logger.info(f"Fetching OHLCV data for {ticker} from {start_date} to {end_date}")

        df = stock.get_market_ohlcv_by_date(
            fromdate=start_date, todate=end_date, ticker=ticker, adjusted=adjusted
        )

        if df.empty:
            return {
                "error": f"No data found for ticker {ticker} in the specified date range",
                "ticker": ticker,
                "start_date": start_date,
                "end_date": end_date,
            }

        # Convert DataFrame to dictionary format
        result = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "adjusted": adjusted,
            "data": df.reset_index().to_dict(orient="records"),
        }

        logger.info(f"Successfully retrieved {len(df)} rows of data")
        return result

    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return {
            "error": str(e),
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
        }


def main():
    """Entry point for the MCP server."""
    logger.info("Starting pykrx-mcp server")
    mcp.run()


if __name__ == "__main__":
    main()
