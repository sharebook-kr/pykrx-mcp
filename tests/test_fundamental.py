"""Tests for fundamental data tools."""

from unittest.mock import patch

import pandas as pd

from pykrx_mcp.tools.fundamental import get_market_fundamental_by_date


class TestGetMarketFundamentalByDate:
    """Test fundamental data retrieval."""

    @patch("pykrx_mcp.tools.fundamental.stock")
    def test_valid_request(self, mock_stock):
        """Should return fundamental data for valid request."""
        mock_df = pd.DataFrame(
            {
                "BPS": [50000, 51000],
                "PER": [15.5, 16.0],
                "PBR": [1.2, 1.3],
                "EPS": [5000, 5100],
                "DIV": [2.5, 2.6],
                "DPS": [1000, 1100],
            }
        )
        mock_stock.get_market_fundamental_by_date.return_value = mock_df

        result = get_market_fundamental_by_date("005930", "20240101", "20240105")

        mock_stock.get_market_fundamental_by_date.assert_called_once_with(
            fromdate="20240101", todate="20240105", ticker="005930"
        )
        assert result["ticker"] == "005930"
        assert result["start_date"] == "20240101"
        assert result["end_date"] == "20240105"
        assert result["row_count"] == 2
        assert len(result["data"]) == 2

    @patch("pykrx_mcp.tools.fundamental.stock")
    def test_invalid_ticker_format(self, mock_stock):
        """Should reject invalid ticker format."""
        result = get_market_fundamental_by_date("5930", "20240101", "20240105")

        mock_stock.get_market_fundamental_by_date.assert_not_called()
        assert "error" in result
        assert "6-digit" in result["error"]

    @patch("pykrx_mcp.tools.fundamental.stock")
    def test_invalid_start_date(self, mock_stock):
        """Should reject invalid start date format."""
        result = get_market_fundamental_by_date("005930", "2024-01-01", "20240105")

        mock_stock.get_market_fundamental_by_date.assert_not_called()
        assert "error" in result
        assert "YYYYMMDD" in result["error"]

    @patch("pykrx_mcp.tools.fundamental.stock")
    def test_empty_dataframe(self, mock_stock):
        """Should handle empty DataFrame."""
        mock_stock.get_market_fundamental_by_date.return_value = pd.DataFrame()

        result = get_market_fundamental_by_date("999999", "20240101", "20240105")

        assert "error" in result
        assert "No fundamental data found" in result["error"]

    @patch("pykrx_mcp.tools.fundamental.stock")
    def test_pykrx_exception(self, mock_stock):
        """Should handle pykrx exceptions."""
        mock_stock.get_market_fundamental_by_date.side_effect = Exception(
            "Network error"
        )

        result = get_market_fundamental_by_date("005930", "20240101", "20240105")

        assert "error" in result
        assert "Network error" in result["error"]
