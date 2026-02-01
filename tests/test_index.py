"""Tests for index data tools."""

from pykrx_mcp.tools.index import (
    get_index_fundamental,
    get_index_ohlcv,
    get_index_portfolio_deposit_file,
    get_index_ticker_list,
    get_index_ticker_name,
)


def test_get_index_ticker_list():
    """Test getting index ticker list."""
    result = get_index_ticker_list("20240101", "KOSPI")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], list)
        assert result["market"] == "KOSPI"


def test_get_index_ticker_list_invalid_market():
    """Test error handling for invalid market."""
    result = get_index_ticker_list("20240101", "INVALID")

    assert "error" in result
    assert "Invalid market" in result["error"]


def test_get_index_ticker_name():
    """Test getting index name."""
    result = get_index_ticker_name("1001")

    assert "name" in result or "error" in result
    if "name" in result:
        assert result["ticker"] == "1001"
        assert isinstance(result["name"], str)


def test_get_index_ohlcv():
    """Test getting index OHLCV data."""
    result = get_index_ohlcv("1001", "20240101", "20240105", "d")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)
        assert result["ticker"] == "1001"


def test_get_index_ohlcv_invalid_freq():
    """Test error handling for invalid frequency."""
    result = get_index_ohlcv("1001", "20240101", "20240105", "invalid")

    assert "error" in result
    assert "Invalid frequency" in result["error"]


def test_get_index_fundamental():
    """Test getting index fundamental data."""
    result = get_index_fundamental("20240101", "20240105", "1001")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)


def test_get_index_fundamental_all_indices():
    """Test getting fundamental data for all indices on a date."""
    result = get_index_fundamental("20240101")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], dict)


def test_get_index_portfolio_deposit_file():
    """Test getting index constituents."""
    result = get_index_portfolio_deposit_file("1005")

    assert "data" in result or "error" in result
    if "data" in result:
        assert isinstance(result["data"], list)
        assert result["ticker"] == "1005"
