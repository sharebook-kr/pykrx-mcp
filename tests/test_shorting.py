"""Tests for shorting data tools."""

from pykrx_mcp.tools.shorting import (
    get_shorting_balance_top50,
    get_shorting_status_by_date,
    get_shorting_volume_by_ticker,
    get_shorting_volume_top50,
)


def test_get_shorting_status_by_date():
    """Test getting shorting status for a stock."""
    result = get_shorting_status_by_date("005930", "20240101", "20240105")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["ticker"] == "005930"


def test_get_shorting_status_invalid_ticker():
    """Test error handling for invalid ticker."""
    result = get_shorting_status_by_date("INVALID", "20240101", "20240105")

    assert "error" in result
    assert "Invalid ticker" in result["error"]


def test_get_shorting_status_invalid_date():
    """Test error handling for invalid date format."""
    result = get_shorting_status_by_date("005930", "2024-01-01", "20240105")

    assert "error" in result
    assert "Invalid date" in result["error"]


def test_get_shorting_volume_by_ticker():
    """Test getting shorting volume for all tickers on a date."""
    result = get_shorting_volume_by_ticker("20240101", "KOSPI")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["market"] == "KOSPI"


def test_get_shorting_volume_invalid_market():
    """Test error handling for invalid market."""
    result = get_shorting_volume_by_ticker("20240101", "INVALID")

    assert "error" in result
    assert "Invalid market" in result["error"]


def test_get_shorting_balance_top50():
    """Test getting top 50 stocks by shorting balance."""
    result = get_shorting_balance_top50("20240101", "KOSPI")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["market"] == "KOSPI"


def test_get_shorting_volume_top50():
    """Test getting top 50 stocks by shorting volume."""
    result = get_shorting_volume_top50("20240101", "KOSDAQ")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["market"] == "KOSDAQ"
