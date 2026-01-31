"""Tests for trading value tools."""

from unittest.mock import patch

import pandas as pd

from pykrx_mcp.tools.trading_value import get_market_trading_value_by_date


class TestGetMarketTradingValueByDate:
    """Test trading value retrieval for supply/demand analysis."""

    @patch("pykrx_mcp.tools.trading_value.stock")
    def test_valid_request(self, mock_stock):
        """Should return trading value data for valid request."""
        mock_df = pd.DataFrame(
            {
                "금융투자": [500000000, 600000000],
                "보험": [100000000, 150000000],
                "투신": [200000000, 250000000],
                "사모": [-50000000, -100000000],
                "은행": [0, 50000000],
                "기타금융": [10000000, 20000000],
                "연기금등": [300000000, 400000000],
                "기타법인": [-100000000, -150000000],
                "개인": [-800000000, -900000000],
                "외국인": [200000000, 300000000],
                "기타외국인": [50000000, 60000000],
            }
        )
        mock_stock.get_market_trading_value_by_date.return_value = mock_df

        result = get_market_trading_value_by_date("005930", "20240101", "20240105")

        mock_stock.get_market_trading_value_by_date.assert_called_once_with(
            fromdate="20240101", todate="20240105", ticker="005930"
        )
        assert result["ticker"] == "005930"
        assert result["start_date"] == "20240101"
        assert result["end_date"] == "20240105"
        assert result["row_count"] == 2

    @patch("pykrx_mcp.tools.trading_value.stock")
    def test_invalid_ticker_format(self, mock_stock):
        """Should reject invalid ticker format."""
        result = get_market_trading_value_by_date("5930", "20240101", "20240105")

        mock_stock.get_market_trading_value_by_date.assert_not_called()
        assert "error" in result
        assert "6-digit" in result["error"]

    @patch("pykrx_mcp.tools.trading_value.stock")
    def test_invalid_start_date(self, mock_stock):
        """Should reject invalid start date format."""
        result = get_market_trading_value_by_date("005930", "2024-01-01", "20240105")

        mock_stock.get_market_trading_value_by_date.assert_not_called()
        assert "error" in result
        assert "YYYYMMDD" in result["error"]

    @patch("pykrx_mcp.tools.trading_value.stock")
    def test_invalid_end_date(self, mock_stock):
        """Should reject invalid end date format."""
        result = get_market_trading_value_by_date("005930", "20240101", "2024-01-05")

        mock_stock.get_market_trading_value_by_date.assert_not_called()
        assert "error" in result
        assert "YYYYMMDD" in result["error"]

    @patch("pykrx_mcp.tools.trading_value.stock")
    def test_empty_dataframe(self, mock_stock):
        """Should handle empty DataFrame."""
        mock_stock.get_market_trading_value_by_date.return_value = pd.DataFrame()

        result = get_market_trading_value_by_date("999999", "20240101", "20240105")

        assert "error" in result
        assert "No trading value data found" in result["error"]

    @patch("pykrx_mcp.tools.trading_value.stock")
    def test_pykrx_exception(self, mock_stock):
        """Should handle pykrx exceptions."""
        mock_stock.get_market_trading_value_by_date.side_effect = Exception(
            "Network error"
        )

        result = get_market_trading_value_by_date("005930", "20240101", "20240105")

        assert "error" in result
        assert "Network error" in result["error"]
