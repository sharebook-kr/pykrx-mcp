"""
REST API wrapper for ChatGPT Actions.

This provides a FastAPI REST API that wraps pykrx-mcp tools
for use with ChatGPT Custom GPT Actions.
"""

import logging
import sys

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

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
    servers=[
        {
            "url": "https://absolute-squid-sharebook-05d10e18.koyeb.app",
            "description": "Production server"
        }
    ],
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
    ticker: str = Field(..., description="6-digit stock ticker code (e.g., '005930')")
    start_date: str = Field(..., description="Start date in YYYYMMDD format (e.g., '20240101')")
    end_date: str = Field(..., description="End date in YYYYMMDD format (e.g., '20240131')")
    adjusted: bool = Field(True, description="Whether to adjust for stock splits")


class TickerListRequest(BaseModel):
    date: str = Field(..., description="Date in YYYYMMDD format (e.g., '20240101')")
    market: str = Field("KOSPI", description="Market type: 'KOSPI', 'KOSDAQ', or 'KONEX'")


class TickerNameRequest(BaseModel):
    ticker: str = Field(..., description="6-digit stock ticker code (e.g., '005930')")


class MarketCapRequest(BaseModel):
    ticker: str = Field(..., description="6-digit stock ticker code (e.g., '005930')")
    start_date: str = Field(..., description="Start date in YYYYMMDD format (e.g., '20240101')")
    end_date: str = Field(..., description="End date in YYYYMMDD format (e.g., '20240131')")


class FundamentalRequest(BaseModel):
    ticker: str = Field(..., description="6-digit stock ticker code (e.g., '005930')")
    start_date: str = Field(..., description="Start date in YYYYMMDD format (e.g., '20240101')")
    end_date: str = Field(..., description="End date in YYYYMMDD format (e.g., '20240131')")


class TradingValueRequest(BaseModel):
    ticker: str = Field(..., description="6-digit stock ticker code (e.g., '005930')")
    start_date: str = Field(..., description="Start date in YYYYMMDD format (e.g., '20240101')")
    end_date: str = Field(..., description="End date in YYYYMMDD format (e.g., '20240131')")


class ETFOHLCVRequest(BaseModel):
    ticker: str = Field(..., description="ETF ticker code (e.g., '152100' for KODEX 레버리지)")
    start_date: str = Field(..., description="Start date in YYYYMMDD format (e.g., '20240101')")
    end_date: str = Field(..., description="End date in YYYYMMDD format (e.g., '20240131')")


class ETFTickerListRequest(BaseModel):
    date: str = Field(..., description="Date in YYYYMMDD format (e.g., '20240101')")


# Endpoints
@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy():
    """Privacy policy page for ChatGPT Actions."""
    return """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>개인정보 보호 정책 - pykrx-mcp</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
                    'Helvetica Neue', Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                color: #333;
            }
            h1 {
                color: #2c3e50;
                border-bottom: 2px solid #3498db;
                padding-bottom: 10px;
            }
            h2 {
                color: #34495e;
                margin-top: 30px;
            }
            .section {
                margin: 20px 0;
            }
            .highlight {
                background-color: #f8f9fa;
                padding: 15px;
                border-left: 4px solid #3498db;
                margin: 15px 0;
            }
            ul {
                padding-left: 20px;
            }
            li {
                margin: 8px 0;
            }
            .footer {
                margin-top: 40px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                color: #7f8c8d;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <h1>개인정보 보호 정책</h1>

        <div class="highlight">
            <strong>최종 업데이트:</strong> 2024년 1월<br>
            <strong>서비스명:</strong> pykrx-mcp (Korean Stock Market Data API)
        </div>

        <div class="section">
            <h2>1. 개요</h2>
            <p>
                pykrx-mcp는 한국 주식 시장의 공개 데이터를 제공하는 API 서비스입니다.
                본 서비스는 <strong>개인정보를 수집, 저장, 처리하지 않습니다</strong>.
            </p>
        </div>

        <div class="section">
            <h2>2. 수집하지 않는 정보</h2>
            <p>본 서비스는 다음과 같은 개인정보를 수집하지 않습니다:</p>
            <ul>
                <li>이름, 이메일, 전화번호 등 개인 식별 정보</li>
                <li>로그인 자격 증명 (사용자 인증 불필요)</li>
                <li>결제 정보 (무료 서비스)</li>
                <li>위치 정보</li>
                <li>쿠키 또는 추적 기술</li>
                <li>IP 주소 (접속 로그 미수집)</li>
            </ul>
        </div>

        <div class="section">
            <h2>3. 제공하는 데이터</h2>
            <p>본 서비스는 다음과 같은 공개 시장 데이터만을 제공합니다:</p>
            <ul>
                <li>주식 가격 정보 (OHLCV)</li>
                <li>시가총액 및 거래량</li>
                <li>투자자별 매매 동향</li>
                <li>기업 기본 정보 (PER, PBR 등)</li>
                <li>ETF 정보</li>
            </ul>
            <p>모든 데이터는 한국거래소(KRX)의 공개 데이터를 기반으로 합니다.</p>
        </div>

        <div class="section">
            <h2>4. 데이터 보안</h2>
            <ul>
                <li>본 서비스는 사용자 데이터베이스를 운영하지 않습니다</li>
                <li>사용자 세션을 저장하지 않습니다</li>
                <li>제3자와 어떠한 정보도 공유하지 않습니다</li>
                <li>HTTPS를 통한 안전한 통신을 지원합니다</li>
            </ul>
        </div>

        <div class="section">
            <h2>5. ChatGPT Actions 사용</h2>
            <p>
                본 API를 ChatGPT Custom GPT Actions와 함께 사용할 때:
            </p>
            <ul>
                <li>OpenAI의 개인정보 보호 정책이 적용됩니다</li>
                <li>ChatGPT와의 대화 내용은 OpenAI가 관리합니다</li>
                <li>본 API는 요청된 시장 데이터만을 반환합니다</li>
                <li>대화 내용이나 사용자 정보를 저장하지 않습니다</li>
            </ul>
        </div>

        <div class="section">
            <h2>6. 오픈소스</h2>
            <p>
                본 프로젝트는 MIT 라이선스의 오픈소스 소프트웨어입니다.
                소스 코드는 GitHub에서 공개적으로 확인할 수 있습니다:
            </p>
            <p>
                <a href="https://github.com/sharebook-kr/pykrx-mcp" target="_blank">
                    https://github.com/sharebook-kr/pykrx-mcp
                </a>
            </p>
        </div>

        <div class="section">
            <h2>7. 면책 조항</h2>
            <ul>
                <li>본 서비스는 투자 조언을 제공하지 않습니다</li>
                <li>제공된 데이터의 정확성을 보증하지 않습니다</li>
                <li>투자 결정에 대한 책임은 사용자에게 있습니다</li>
                <li>실시간 데이터가 아닌 종가 기준 데이터입니다</li>
            </ul>
        </div>

        <div class="section">
            <h2>8. 연락처</h2>
            <p>
                서비스에 대한 문의사항이 있으시면 GitHub Issues를 통해 연락해주세요:<br>
                <a
                    href="https://github.com/sharebook-kr/pykrx-mcp/issues"
                    target="_blank"
                >
                    https://github.com/sharebook-kr/pykrx-mcp/issues
                </a>
            </p>
        </div>

        <div class="section">
            <h2>9. 정책 변경</h2>
            <p>
                본 개인정보 보호 정책은 필요에 따라 업데이트될 수 있습니다.
                중요한 변경 사항이 있을 경우 GitHub 리포지토리를 통해 공지됩니다.
            </p>
        </div>

        <div class="footer">
            <p>
                <strong>pykrx-mcp</strong> - Korean Stock Market Data API<br>
                Powered by
                <a href="https://github.com/sharebook-kr/pykrx" target="_blank">
                    pykrx
                </a>
                library
            </p>
        </div>
    </body>
    </html>
    """


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
        logger.info(f"Fetching market cap for {request.ticker}")
        result = get_market_cap_impl(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=request.end_date,
        )
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
        logger.info(f"Fetching fundamental data for {request.ticker}")
        result = get_fundamental_impl(
            ticker=request.ticker,
            start_date=request.start_date,
            end_date=request.end_date,
        )
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
