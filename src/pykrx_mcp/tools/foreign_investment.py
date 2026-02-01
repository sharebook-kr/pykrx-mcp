"""외국인 보유량 및 한도소진률 조회 도구."""

# Configure logging to stderr
import logging
from typing import Any

from pykrx import stock

from ..utils.decorators import handle_pykrx_errors
from ..utils.formatters import dict_to_table
from ..utils.validators import validate_date_format, validate_ticker

logger = logging.getLogger(__name__)


@handle_pykrx_errors
def get_exhaustion_rates_of_foreign_investment(
    start_date: str,
    end_date: str = None,
    ticker: str = None,
    market: str = "KOSPI",
    balance_limit: bool = False,
) -> dict[str, Any]:
    """
    외국인 보유량 및 한도소진률을 조회합니다.

    Args:
        start_date: 조회 시작일 (YYYYMMDD 형식, 예: '20240101')
        end_date: 조회 종료일 (YYYYMMDD 형식, ticker와 함께 사용)
        ticker: 종목코드 (6자리, end_date와 함께 사용 시 일자별 조회)
        market: 시장 구분 (KOSPI/KOSDAQ/KONEX, 기본값: KOSPI)
        balance_limit: 외국인 보유한도 제한 종목만 조회 여부

    Returns:
        Dict containing:
        - data: 상장주식수/보유수량/지분율/한도수량/한도소진률
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(
        f"Fetching foreign investment rates for {ticker or market} "
        f"from {start_date} to {end_date or start_date}"
    )

    if not validate_date_format(start_date):
        return {
            "error": "Invalid start_date format. Use YYYYMMDD (e.g., '20240101').",
            "start_date": start_date,
        }

    if end_date and ticker:
        # 일자별 특정 종목 조회
        if not validate_date_format(end_date):
            return {
                "error": "Invalid end_date format. Use YYYYMMDD (e.g., '20240131').",
                "end_date": end_date,
            }
        if not validate_ticker(ticker):
            return {
                "error": "Invalid ticker format. Must be 6 digits.",
                "ticker": ticker,
            }

        df = stock.get_exhaustion_rates_of_foreign_investment(
            start_date, end_date, ticker
        )

        if df.empty:
            return {
                "error": "No data found for the given period.",
                "ticker": ticker,
                "start_date": start_date,
                "end_date": end_date,
            }

        # Convert to dict with date as string
        result_dict = df.to_dict(orient="index")
        formatted_dict = {str(k): v for k, v in result_dict.items()}

        return {
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
            "data": formatted_dict,
            "table": dict_to_table(formatted_dict),
        }

    else:
        # 특정 일자의 전종목 조회
        market_upper = market.upper()
        if market_upper not in ["KOSPI", "KOSDAQ", "KONEX"]:
            return {
                "error": "Invalid market. Must be one of: KOSPI, KOSDAQ, KONEX",
                "market": market,
            }

        df = stock.get_exhaustion_rates_of_foreign_investment(
            start_date, market=market_upper, balance_limit=balance_limit
        )

        if df.empty:
            return {
                "error": "No data found for the given date.",
                "date": start_date,
                "market": market,
            }

        # Convert to dict with ticker as key
        result_dict = df.to_dict(orient="index")
        formatted_dict = {str(k): v for k, v in result_dict.items()}

        return {
            "date": start_date,
            "market": market_upper,
            "balance_limit": balance_limit,
            "data": formatted_dict,
            "table": dict_to_table(formatted_dict),
        }
