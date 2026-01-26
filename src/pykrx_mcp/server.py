import sys
from datetime import datetime, timedelta
from mcp.server.fastmcp import FastMCP
from pykrx import stock


# Initialize FastMCP server
mcp = FastMCP("pykrx-mcp")


# Configure logging to stderr (MCP uses stdout for protocol communication)
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger(__name__)


@mcp.tool()
def get_stock_ohlcv(
    ticker: str,
    start_date: str,
    end_date: str,
    adjusted: bool = True
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
            fromdate=start_date,
            todate=end_date,
            ticker=ticker,
            adjusted=adjusted
        )
        
        if df.empty:
            return {
                "error": f"No data found for ticker {ticker} in the specified date range",
                "ticker": ticker,
                "start_date": start_date,
                "end_date": end_date
            }
        
        # Convert DataFrame to dictionary format
        result = {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "adjusted": adjusted,
            "data": df.reset_index().to_dict(orient='records')
        }
        
        logger.info(f"Successfully retrieved {len(df)} rows of data")
        return result
        
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        return {
            "error": str(e),
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date
        }


def main():
    """Entry point for the MCP server."""
    logger.info("Starting pykrx-mcp server")
    mcp.run()


if __name__ == "__main__":
    main()
