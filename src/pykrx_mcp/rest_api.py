"""
REST API wrapper for ChatGPT Actions.

This provides a FastAPI REST API that wraps pykrx-mcp tools
for use with ChatGPT Custom GPT Actions.
"""

import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from pykrx_mcp.tools.etf_price import (
    get_etf_ohlcv_by_date as get_etf_ohlcv_impl,
)
from pykrx_mcp.tools.etf_price import (
    get_etf_ticker_list as get_etf_ticker_list_impl,
)
from pykrx_mcp.tools.fundamental import (
    get_market_fundamental_by_date as get_fundamental_impl,
)
from pykrx_mcp.tools.market_cap import get_market_cap_by_date as get_market_cap_impl

# Import MCP tools
from pykrx_mcp.tools.stock_price import get_stock_ohlcv as get_stock_ohlcv_impl
from pykrx_mcp.tools.ticker_info import (
    get_market_ticker_list as get_ticker_list_impl,
)
from pykrx_mcp.tools.ticker_info import (
    get_market_ticker_name as get_ticker_name_impl,
)
from pykrx_mcp.tools.trading_value import (
    get_market_trading_value_by_date as get_trading_value_impl,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="pykrx-mcp REST API",
    description="Korean stock market data API for ChatGPT Actions",
    version="0.5.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request models
class StockOHLCVRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str
    adjusted: bool = True


class TickerListRequest(BaseModel):
    date: str
    market: str = "KOSPI"


class TickerNameRequest(BaseModel):
    ticker: str


class MarketCapRequest(BaseModel):
    date: str
    market: str = "KOSPI"


class FundamentalRequest(BaseModel):
    date: str
    market: str = "KOSPI"


class TradingValueRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str


class ETFOHLCVRequest(BaseModel):
    ticker: str
    start_date: str
    end_date: str


class ETFTickerListRequest(BaseModel):
    date: str


# Endpoints
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/tools/get_stock_ohlcv")
async def get_stock_ohlcv(request: StockOHLCVRequest):
    """Get stock OHLCV data."""
    try:
        logger.info(f"Fetching OHLCV for {request.ticker}")
        result = get_stock_ohlcv_impl(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=request.end_date,
            adjusted=request.adjusted,
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_stock_ohlcv: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/tools/get_market_ticker_list")
async def get_market_ticker_list(request: TickerListRequest):
    """Get list of stock tickers."""
    try:
        logger.info(f"Fetching ticker list for {request.market}")
        result = get_ticker_list_impl(date=request.date, market=request.market)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_market_ticker_list: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/tools/get_market_ticker_name")
async def get_market_ticker_name(request: TickerNameRequest):
    """Get company name from ticker."""
    try:
        logger.info(f"Fetching name for {request.ticker}")
        result = get_ticker_name_impl(ticker=request.ticker)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_market_ticker_name: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/tools/get_market_cap_by_date")
async def get_market_cap_by_date(request: MarketCapRequest):
    """Get market cap data."""
    try:
        logger.info(f"Fetching market cap for {request.market}")
        result = get_market_cap_impl(date=request.date, market=request.market)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_market_cap_by_date: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/tools/get_market_fundamental_by_date")
async def get_market_fundamental_by_date(request: FundamentalRequest):
    """Get fundamental data."""
    try:
        logger.info(f"Fetching fundamental data for {request.market}")
        result = get_fundamental_impl(date=request.date, market=request.market)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_market_fundamental_by_date: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/tools/get_market_trading_value_by_date")
async def get_market_trading_value_by_date(request: TradingValueRequest):
    """Get investor trading value (supply/demand analysis)."""
    try:
        logger.info(f"Fetching trading value for {request.ticker}")
        result = get_trading_value_impl(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_market_trading_value_by_date: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/tools/get_etf_ohlcv_by_date")
async def get_etf_ohlcv_by_date(request: ETFOHLCVRequest):
    """Get ETF OHLCV data."""
    try:
        logger.info(f"Fetching ETF OHLCV for {request.ticker}")
        result = get_etf_ohlcv_impl(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=request.end_date,
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_etf_ohlcv_by_date: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


@app.post("/tools/get_etf_ticker_list")
async def get_etf_ticker_list(request: ETFTickerListRequest):
    """Get list of ETF tickers."""
    try:
        logger.info(f"Fetching ETF ticker list for {request.date}")
        result = get_etf_ticker_list_impl(date=request.date)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        logger.error(f"Error in get_etf_ticker_list: {e}")
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
