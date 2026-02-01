"""Tests for investor trading data tools."""

from pykrx_mcp.tools.investor import (
    get_market_net_purchases_of_equities,
    get_market_trading_value_by_investor,
    get_market_trading_volume_by_investor,
)


def test_get_market_trading_volume_by_investor_stock():
    """Test getting investor trading volume for a stock."""
    result = get_market_trading_volume_by_investor("20240101", "20240105", "005930")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["ticker"] == "005930"


def test_get_market_trading_volume_by_investor_market():
    """Test getting investor trading volume for a market."""
    result = get_market_trading_volume_by_investor("20240101", "20240105", "KOSPI")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["ticker"] == "KOSPI"


def test_get_market_trading_value_by_investor():
    """Test getting investor trading value."""
    result = get_market_trading_value_by_investor("20240101", "20240105", "KOSDAQ")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)


def test_get_market_net_purchases_of_equities():
    """Test getting net purchases by investor type."""
    result = get_market_net_purchases_of_equities(
        "20240101", "20240105", "KOSPI", "외국인"
    )

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["market"] == "KOSPI"
        assert result["investor"] == "외국인"


def test_get_market_net_purchases_invalid_market():
    """Test error handling for invalid market."""
    result = get_market_net_purchases_of_equities(
        "20240101", "20240105", "INVALID", "외국인"
    )

    assert "error" in result
    assert "Invalid market" in result["error"]


def test_get_market_net_purchases_invalid_investor():
    """Test error handling for invalid investor type."""
    result = get_market_net_purchases_of_equities(
        "20240101", "20240105", "KOSPI", "INVALID"
    )

    assert "error" in result
    assert "Invalid investor" in result["error"]
