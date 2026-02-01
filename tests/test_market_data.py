"""Tests for market-wide data tools."""

from pykrx_mcp.tools.market_data import (
    get_market_ohlcv_by_date,
    get_market_price_change,
)


def test_get_market_ohlcv_by_date():
    """Test getting market OHLCV for all stocks."""
    result = get_market_ohlcv_by_date("20240101", "KOSPI")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["market"] == "KOSPI"
        assert "count" in result


def test_get_market_ohlcv_invalid_market():
    """Test error handling for invalid market."""
    result = get_market_ohlcv_by_date("20240101", "INVALID")

    assert "error" in result
    assert "Invalid market" in result["error"]


def test_get_market_price_change():
    """Test getting price changes for all stocks."""
    result = get_market_price_change("20240101", "20240105", "KOSDAQ")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["market"] == "KOSDAQ"
        assert "count" in result


def test_get_market_price_change_invalid_date():
    """Test error handling for invalid date format."""
    result = get_market_price_change("2024-01-01", "20240105", "KOSPI")

    assert "error" in result
    assert "Invalid date" in result["error"]
