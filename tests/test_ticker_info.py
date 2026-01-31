"""Tests for ticker info tools."""

from unittest.mock import patch

from pykrx_mcp.tools.ticker_info import (
    get_market_ticker_list,
    get_market_ticker_name,
)


class TestGetMarketTickerList:
    """Test market ticker list retrieval."""

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_valid_kospi_request(self, mock_stock):
        """Should return KOSPI ticker list for valid request."""
        mock_stock.get_market_ticker_list.return_value = [
            "005930",
            "000660",
            "035420",
        ]

        result = get_market_ticker_list("20240101", "KOSPI")

        mock_stock.get_market_ticker_list.assert_called_once_with(
            "20240101", market="KOSPI"
        )
        assert result["date"] == "20240101"
        assert result["market"] == "KOSPI"
        assert result["count"] == 3
        assert "005930" in result["tickers"]

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_valid_kosdaq_request(self, mock_stock):
        """Should return KOSDAQ ticker list."""
        mock_stock.get_market_ticker_list.return_value = ["035720", "036570"]

        result = get_market_ticker_list("20240101", "KOSDAQ")

        assert result["market"] == "KOSDAQ"
        assert result["count"] == 2

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_invalid_date_format(self, mock_stock):
        """Should reject invalid date format."""
        result = get_market_ticker_list("2024-01-01", "KOSPI")

        mock_stock.get_market_ticker_list.assert_not_called()
        assert "error" in result
        assert "YYYYMMDD" in result["error"]

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_invalid_market(self, mock_stock):
        """Should reject invalid market name."""
        result = get_market_ticker_list("20240101", "NYSE")

        mock_stock.get_market_ticker_list.assert_not_called()
        assert "error" in result
        assert "NYSE" in result["error"]

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_empty_ticker_list(self, mock_stock):
        """Should handle empty ticker list."""
        mock_stock.get_market_ticker_list.return_value = []

        result = get_market_ticker_list("20240101", "KOSPI")

        assert "error" in result
        assert "No tickers found" in result["error"]


class TestGetMarketTickerName:
    """Test ticker name retrieval."""

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_valid_ticker(self, mock_stock):
        """Should return company name for valid ticker."""
        mock_stock.get_market_ticker_name.return_value = "삼성전자"

        result = get_market_ticker_name("005930")

        mock_stock.get_market_ticker_name.assert_called_once_with("005930")
        assert result["ticker"] == "005930"
        assert result["name"] == "삼성전자"

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_invalid_ticker_format(self, mock_stock):
        """Should reject invalid ticker format."""
        result = get_market_ticker_name("5930")

        mock_stock.get_market_ticker_name.assert_not_called()
        assert "error" in result
        assert "6-digit" in result["error"]

    @patch("pykrx_mcp.tools.ticker_info.stock")
    def test_ticker_not_found(self, mock_stock):
        """Should handle ticker not found."""
        mock_stock.get_market_ticker_name.return_value = ""

        result = get_market_ticker_name("999999")

        assert "error" in result
        assert "not found" in result["error"]
