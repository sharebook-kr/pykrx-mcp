"""지수(Index) 데이터 조회 도구."""

# Configure logging to stderr
import logging
from typing import Any

from pykrx import stock

from ..utils.decorators import handle_pykrx_errors
from ..utils.formatters import dict_to_table
from ..utils.validators import validate_date_format

logger = logging.getLogger(__name__)


@handle_pykrx_errors
def get_index_ticker_list(date: str = None, market: str = "KOSPI") -> dict[str, Any]:
    """
    지수(인덱스) 티커 목록을 조회합니다.

    Args:
        date: 조회 일자 (YYYYMMDD 형식, 생략 시 최근 영업일)
        market: 시장 구분 (KOSPI/KOSDAQ, 기본값: KOSPI)

    Returns:
        Dict containing:
        - data: 지수 티커 리스트
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(f"Fetching index ticker list for {market} on {date or 'latest'}")

    if date and not validate_date_format(date):
        return {
            "error": "Invalid date format. Use YYYYMMDD (e.g., '20240101').",
            "date": date,
        }

    market_upper = market.upper()
    if market_upper not in ["KOSPI", "KOSDAQ"]:
        return {
            "error": "Invalid market. Must be one of: KOSPI, KOSDAQ",
            "market": market,
        }

    if date:
        tickers = stock.get_index_ticker_list(date, market=market_upper)
    else:
        tickers = stock.get_index_ticker_list(market=market_upper)

    if not tickers:
        return {"error": "No index tickers found.", "date": date, "market": market}

    return {
        "date": date or "latest",
        "market": market_upper,
        "data": tickers,
        "count": len(tickers),
    }


@handle_pykrx_errors
def get_index_ticker_name(ticker: str) -> dict[str, Any]:
    """
    지수 티커의 이름을 조회합니다.

    Args:
        ticker: 지수 티커 (예: '1001')

    Returns:
        Dict containing:
        - name: 지수 이름
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(f"Fetching index name for {ticker}")

    if not ticker:
        return {"error": "Ticker is required.", "ticker": ticker}

    name = stock.get_index_ticker_name(ticker)

    if not name:
        return {"error": "Index name not found.", "ticker": ticker}

    return {"ticker": ticker, "name": name}


@handle_pykrx_errors
def get_index_ohlcv(
    ticker: str, start_date: str, end_date: str, freq: str = "d"
) -> dict[str, Any]:
    """
    지수의 OHLCV를 조회합니다.

    Args:
        ticker: 지수 티커 (예: '1001' - 코스피)
        start_date: 조회 시작일 (YYYYMMDD 형식, 예: '20240101')
        end_date: 조회 종료일 (YYYYMMDD 형식, 예: '20240131')
        freq: 조회 주기 (d: 일별, m: 월별, y: 연별, 기본값: d)

    Returns:
        Dict containing:
        - data: 일자별 시가/고가/저가/종가/거래량
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(
        f"Fetching index OHLCV for {ticker} from {start_date} to {end_date} ({freq})"
    )

    if not validate_date_format(start_date) or not validate_date_format(end_date):
        return {
            "error": "Invalid date format. Use YYYYMMDD (e.g., '20240101').",
            "start_date": start_date,
            "end_date": end_date,
        }

    if freq not in ["d", "m", "y"]:
        return {"error": "Invalid frequency. Must be one of: d, m, y", "freq": freq}

    df = stock.get_index_ohlcv(start_date, end_date, ticker, freq=freq)

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
        "frequency": freq,
        "data": formatted_dict,
        "table": dict_to_table(formatted_dict),
    }


@handle_pykrx_errors
def get_index_fundamental(
    start_date: str, end_date: str = None, ticker: str = None
) -> dict[str, Any]:
    """
    지수의 fundamental 정보(PER/PBR/배당수익률)를 조회합니다.

    Args:
        start_date: 조회 시작일 (YYYYMMDD 형식)
        end_date: 조회 종료일 (YYYYMMDD 형식, 생략 시 start_date의 모든 지수)
        ticker: 지수 티커 (예: '1001', end_date와 함께 사용)

    Returns:
        Dict containing:
        - data: 지수별/일자별 PER/PBR/배당수익률
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(
        f"Fetching index fundamental for {ticker or 'all'} "
        f"from {start_date} to {end_date or start_date}"
    )

    if not validate_date_format(start_date):
        return {
            "error": "Invalid start_date format. Use YYYYMMDD (e.g., '20240101').",
            "start_date": start_date,
        }

    if end_date:
        if not validate_date_format(end_date):
            return {
                "error": "Invalid end_date format. Use YYYYMMDD (e.g., '20240131').",
                "end_date": end_date,
            }
        if not ticker:
            return {
                "error": "ticker is required when end_date is provided.",
                "start_date": start_date,
                "end_date": end_date,
            }
        df = stock.get_index_fundamental(start_date, end_date, ticker)
    else:
        df = stock.get_index_fundamental(start_date)

    if df.empty:
        return {
            "error": "No data found.",
            "start_date": start_date,
            "end_date": end_date,
            "ticker": ticker,
        }

    # Convert to dict with date/index name as string
    result_dict = df.to_dict(orient="index")
    formatted_dict = {str(k): v for k, v in result_dict.items()}

    return {
        "start_date": start_date,
        "end_date": end_date,
        "ticker": ticker,
        "data": formatted_dict,
        "table": dict_to_table(formatted_dict),
    }


@handle_pykrx_errors
def get_index_portfolio_deposit_file(ticker: str, date: str = None) -> dict[str, Any]:
    """
    지수를 구성하는 종목 티커를 조회합니다.

    Args:
        ticker: 지수 티커 (예: '1005' - 섬유의복)
        date: 조회 일자 (YYYYMMDD 형식, 생략 시 최근)

    Returns:
        Dict containing:
        - data: 구성 종목 티커 리스트
        - error: 오류 발생 시 오류 메시지
    """
    logger.info(f"Fetching index portfolio for {ticker} on {date or 'latest'}")

    if date and not validate_date_format(date):
        return {
            "error": "Invalid date format. Use YYYYMMDD (e.g., '20240101').",
            "date": date,
        }

    if date:
        tickers = stock.get_index_portfolio_deposit_file(ticker, date)
    else:
        tickers = stock.get_index_portfolio_deposit_file(ticker)

    if not tickers:
        return {"error": "No constituents found.", "ticker": ticker, "date": date}

    return {
        "ticker": ticker,
        "date": date or "latest",
        "data": tickers,
        "count": len(tickers),
    }
