"""전체 종목 시세 조회 도구."""

# Configure logging to stderr
import logging
from typing import Any

from pykrx import stock

from ..utils.decorators import handle_pykrx_errors
from ..utils.formatters import dict_to_table
from ..utils.validators import validate_date_format

logger = logging.getLogger(__name__)


@handle_pykrx_errors
def get_market_ohlcv_by_date(date: str, market: str = "KOSPI") -> dict[str, Any]:
    """
    특정 일자의 전종목 시세를 조회합니다.

    Args:
        date: 조회 일자 (YYYYMMDD 형식, 예: '20240101')
        market: 시장 구분 (KOSPI/KOSDAQ/KONEX/ALL, 기본값: KOSPI)

    Returns:
        Dict containing:
        - data: 종목별 시가/고가/저가/종가/거래량/거래대금/등락률
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(f"Fetching market OHLCV for {market} on {date}")

    if not validate_date_format(date):
        return {
            "error": "Invalid date format. Use YYYYMMDD (e.g., '20240101').",
            "date": date,
        }

    market_upper = market.upper()
    if market_upper not in ["KOSPI", "KOSDAQ", "KONEX", "ALL"]:
        return {
            "error": "Invalid market. Must be one of: KOSPI, KOSDAQ, KONEX, ALL",
            "market": market,
        }

    df = stock.get_market_ohlcv(date, market=market_upper)

    if df.empty:
        return {
            "error": "No data found for the given date.",
            "date": date,
            "market": market,
        }

    # Convert to dict with ticker as key
    result_dict = df.to_dict(orient="index")
    formatted_dict = {str(k): v for k, v in result_dict.items()}

    return {
        "date": date,
        "market": market_upper,
        "data": formatted_dict,
        "table": dict_to_table(formatted_dict),
        "count": len(formatted_dict),
    }


@handle_pykrx_errors
def get_market_price_change(
    start_date: str, end_date: str, market: str = "KOSPI"
) -> dict[str, Any]:
    """
    특정 기간 동안의 전종목 가격 변동을 조회합니다.

    Args:
        start_date: 조회 시작일 (YYYYMMDD 형식, 예: '20240101')
        end_date: 조회 종료일 (YYYYMMDD 형식, 예: '20240131')
        market: 시장 구분 (KOSPI/KOSDAQ/KONEX/ALL, 기본값: KOSPI)

    Returns:
        Dict containing:
        - data: 종목별 시가/종가/변동폭/등락률/거래량/거래대금
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(
        f"Fetching market price change for {market} from {start_date} to {end_date}"
    )

    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return {
            "error": "Invalid date format. Use YYYYMMDD (e.g., '20240101').",
            "start_date": start_date,
            "end_date": end_date,
        }

    market_upper = market.upper()
    if market_upper not in ["KOSPI", "KOSDAQ", "KONEX", "ALL"]:
        return {
            "error": "Invalid market. Must be one of: KOSPI, KOSDAQ, KONEX, ALL",
            "market": market,
        }

    df = stock.get_market_price_change(start_date, end_date, market=market_upper)

    if df.empty:
        return {
            "error": "No data found for the given period.",
            "start_date": start_date,
            "end_date": end_date,
            "market": market,
        }

    # Convert to dict with ticker as key
    result_dict = df.to_dict(orient="index")
    formatted_dict = {str(k): v for k, v in result_dict.items()}

    return {
        "start_date": start_date,
        "end_date": end_date,
        "market": market_upper,
        "data": formatted_dict,
        "table": dict_to_table(formatted_dict),
        "count": len(formatted_dict),
    }
