"""투자자별 거래 현황 조회 도구."""

# Configure logging to stderr
import logging
from typing import Any

from pykrx import stock

from ..utils.decorators import handle_pykrx_errors
from ..utils.formatters import dict_to_table
from ..utils.validators import validate_date_format, validate_ticker

logger = logging.getLogger(__name__)


@handle_pykrx_errors
def get_market_trading_volume_by_investor(
    start_date: str, end_date: str, ticker: str, market: str = None
) -> dict[str, Any]:
    """
    투자자별 순매수 거래량을 조회합니다.

    Args:
        start_date: 조회 시작일 (YYYYMMDD 형식, 예: '20240101')
        end_date: 조회 종료일 (YYYYMMDD 형식, 예: '20240131')
        ticker: 종목코드 또는 시장 구분 (6자리 종목코드 또는 KOSPI/KOSDAQ/KONEX/ALL)
        market: 사용하지 않음 (deprecated, ticker에 시장 구분 직접 입력)

    Returns:
        Dict containing:
        - data: 투자자별 매도/매수/순매수 거래량
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(
        f"Fetching trading volume by investor for {ticker} "
        f"from {start_date} to {end_date}"
    )

    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return {
            "error": "Invalid date format. Use YYYYMMDD (e.g., '20240101').",
            "start_date": start_date,
            "end_date": end_date,
        }

    # Determine if ticker is a stock ticker or market
    ticker_upper = ticker.upper()
    if ticker_upper in ["KOSPI", "KOSDAQ", "KONEX", "ALL"]:
        # Market query
        df = stock.get_market_trading_volume_by_investor(
            start_date, end_date, ticker_upper
        )
    else:
        # Stock ticker query
        if not validate_ticker(ticker):
            return {
                "error": "Invalid ticker format. Must be 6 digits or market name.",
                "ticker": ticker,
            }
        df = stock.get_market_trading_volume_by_investor(start_date, end_date, ticker)

    if df.empty:
        return {
            "error": "No data found for the given period.",
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
        }

    # Convert to dict
    result_dict = df.to_dict(orient="index")
    formatted_dict = {str(k): v for k, v in result_dict.items()}

    return {
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "data": formatted_dict,
        "table": dict_to_table(formatted_dict),
    }


@handle_pykrx_errors
def get_market_trading_value_by_investor(
    start_date: str, end_date: str, ticker: str
) -> dict[str, Any]:
    """
    투자자별 순매수 거래대금을 조회합니다.

    Args:
        start_date: 조회 시작일 (YYYYMMDD 형식, 예: '20240101')
        end_date: 조회 종료일 (YYYYMMDD 형식, 예: '20240131')
        ticker: 종목코드 또는 시장 구분 (6자리 종목코드 또는 KOSPI/KOSDAQ/KONEX/ALL)

    Returns:
        Dict containing:
        - data: 투자자별 매도/매수/순매수 거래대금
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(
        f"Fetching trading value by investor for {ticker} "
        f"from {start_date} to {end_date}"
    )

    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return {
            "error": "Invalid date format. Use YYYYMMDD (e.g., '20240101').",
            "start_date": start_date,
            "end_date": end_date,
        }

    # Determine if ticker is a stock ticker or market
    ticker_upper = ticker.upper()
    if ticker_upper in ["KOSPI", "KOSDAQ", "KONEX", "ALL"]:
        # Market query
        df = stock.get_market_trading_value_by_investor(
            start_date, end_date, ticker_upper
        )
    else:
        # Stock ticker query
        if not validate_ticker(ticker):
            return {
                "error": "Invalid ticker format. Must be 6 digits or market name.",
                "ticker": ticker,
            }
        df = stock.get_market_trading_value_by_investor(start_date, end_date, ticker)

    if df.empty:
        return {
            "error": "No data found for the given period.",
            "ticker": ticker,
            "start_date": start_date,
            "end_date": end_date,
        }

    # Convert to dict
    result_dict = df.to_dict(orient="index")
    formatted_dict = {str(k): v for k, v in result_dict.items()}

    return {
        "ticker": ticker,
        "start_date": start_date,
        "end_date": end_date,
        "data": formatted_dict,
        "table": dict_to_table(formatted_dict),
    }


@handle_pykrx_errors
def get_market_net_purchases_of_equities(
    start_date: str, end_date: str, market: str, investor: str
) -> dict[str, Any]:
    """
    투자자별 순매수 상위 종목을 조회합니다.

    Args:
        start_date: 조회 시작일 (YYYYMMDD 형식, 예: '20240101')
        end_date: 조회 종료일 (YYYYMMDD 형식, 예: '20240131')
        market: 시장 구분 (KOSPI/KOSDAQ/KONEX/ALL)
        investor: 투자자 구분
            (금융투자/보험/투신/사모/은행/기타금융/연기금/기관합계/
            기타법인/개인/외국인/기타외국인/전체)

    Returns:
        Dict containing:
        - data: 종목별 순매수 거래량/거래대금
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(
        f"Fetching net purchases for {investor} in {market} "
        f"from {start_date} to {end_date}"
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

    valid_investors = [
        "금융투자",
        "보험",
        "투신",
        "사모",
        "은행",
        "기타금융",
        "연기금",
        "기관합계",
        "기타법인",
        "개인",
        "외국인",
        "기타외국인",
        "전체",
    ]
    if investor not in valid_investors:
        return {
            "error": f"Invalid investor. Must be one of: {', '.join(valid_investors)}",
            "investor": investor,
        }

    df = stock.get_market_net_purchases_of_equities(
        start_date, end_date, market_upper, investor
    )

    if df.empty:
        return {
            "error": "No data found for the given period.",
            "market": market,
            "investor": investor,
            "start_date": start_date,
            "end_date": end_date,
        }

    # Convert to dict with ticker as key
    result_dict = df.to_dict(orient="index")
    formatted_dict = {str(k): v for k, v in result_dict.items()}

    return {
        "market": market_upper,
        "investor": investor,
        "start_date": start_date,
        "end_date": end_date,
        "data": formatted_dict,
        "table": dict_to_table(formatted_dict),
    }
