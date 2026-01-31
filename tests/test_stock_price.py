"""Tests for stock price tools."""

from unittest.mock import patch

import pandas as pd

from pykrx_mcp.tools.stock_price import get_stock_ohlcv


class TestGetStockOHLCV:
    """Test stock OHLCV retrieval tool."""

    @patch("pykrx_mcp.tools.stock_price.stock")
    def test_valid_request(self, mock_stock):
        """Should return formatted data for valid request."""
        # Mock pykrx response
        mock_df = pd.DataFrame(
            {
                "시가": [70000, 71000],
                "고가": [72000, 73000],
                "저가": [69000, 70000],
                "종가": [71000, 72000],
                "거래량": [1000000, 1100000],
            }
        )
        mock_stock.get_market_ohlcv_by_date.return_value = mock_df

        result = get_stock_ohlcv("005930", "20240101", "20240105", True)

        # Verify pykrx was called correctly
        mock_stock.get_market_ohlcv_by_date.assert_called_once_with(
            fromdate="20240101", todate="20240105", ticker="005930", adjusted=True
        )

        # Verify response structure
        assert "error" not in result
        assert result["ticker"] == "005930"
        assert result["start_date"] == "20240101"
        assert result["end_date"] == "20240105"
        assert result["adjusted"] is True
        assert result["row_count"] == 2
        assert len(result["data"]) == 2

    @patch("pykrx_mcp.tools.stock_price.stock")
    def test_invalid_ticker_format(self, mock_stock):
        """Should reject invalid ticker format."""
        result = get_stock_ohlcv("5930", "20240101", "20240105", True)

        # Should not call pykrx
        mock_stock.get_market_ohlcv_by_date.assert_not_called()

        # Should return validation error
        assert "error" in result
        assert "6-digit" in result["error"]
        assert result["ticker"] == "5930"

    @patch("pykrx_mcp.tools.stock_price.stock")
    def test_invalid_start_date_format(self, mock_stock):
        """Should reject invalid start date format."""
        result = get_stock_ohlcv("005930", "2024-01-01", "20240105", True)

        mock_stock.get_market_ohlcv_by_date.assert_not_called()

        assert "error" in result
        assert "YYYYMMDD" in result["error"]
        assert result["start_date"] == "2024-01-01"

    @patch("pykrx_mcp.tools.stock_price.stock")
    def test_invalid_end_date_format(self, mock_stock):
        """Should reject invalid end date format."""
        result = get_stock_ohlcv("005930", "20240101", "2024-01-05", True)

        mock_stock.get_market_ohlcv_by_date.assert_not_called()

        assert "error" in result
        assert "YYYYMMDD" in result["error"]
        assert result["end_date"] == "2024-01-05"

    @patch("pykrx_mcp.tools.stock_price.stock")
    def test_empty_dataframe(self, mock_stock):
        """Should handle empty DataFrame from pykrx."""
        mock_stock.get_market_ohlcv_by_date.return_value = pd.DataFrame()

        result = get_stock_ohlcv("999999", "20240101", "20240105", True)

        assert "error" in result
        assert "No data found" in result["error"]
        assert result["ticker"] == "999999"

    @patch("pykrx_mcp.tools.stock_price.stock")
    def test_pykrx_exception(self, mock_stock):
        """Should handle pykrx exceptions gracefully."""
        mock_stock.get_market_ohlcv_by_date.side_effect = Exception("Network error")

        result = get_stock_ohlcv("005930", "20240101", "20240105", True)

        assert "error" in result
        assert "Network error" in result["error"]
        assert "function" in result  # From decorator

    @patch("pykrx_mcp.tools.stock_price.stock")
    def test_adjusted_parameter(self, mock_stock):
        """Should pass adjusted parameter correctly."""
        mock_df = pd.DataFrame({"종가": [100]})
        mock_stock.get_market_ohlcv_by_date.return_value = mock_df

        # Test adjusted=False
        result = get_stock_ohlcv("005930", "20240101", "20240105", False)

        mock_stock.get_market_ohlcv_by_date.assert_called_with(
            fromdate="20240101", todate="20240105", ticker="005930", adjusted=False
        )
        assert result["adjusted"] is False
