"""Tests for ETF tools."""

from unittest.mock import patch

import pandas as pd

from pykrx_mcp.tools.etf_price import get_etf_ohlcv_by_date, get_etf_ticker_list


class TestGetEtfOhlcvByDate:
    """Test ETF OHLCV retrieval."""

    @patch("pykrx_mcp.tools.etf_price.stock")
    def test_valid_request(self, mock_etf):
        """Should return ETF OHLCV data for valid request."""
        mock_df = pd.DataFrame(
            {
                "시가": [30000, 30500],
                "고가": [31000, 31500],
                "저가": [29500, 30000],
                "종가": [30500, 31000],
                "거래량": [100000, 110000],
                "NAV": [30400, 30900],
            }
        )
        mock_etf.get_etf_ohlcv_by_date.return_value = mock_df

        result = get_etf_ohlcv_by_date("069500", "20240101", "20240105")

        mock_etf.get_etf_ohlcv_by_date.assert_called_once_with(
            fromdate="20240101", todate="20240105", ticker="069500"
        )
        assert result["ticker"] == "069500"
        assert result["start_date"] == "20240101"
        assert result["end_date"] == "20240105"
        assert result["row_count"] == 2

    @patch("pykrx_mcp.tools.etf_price.stock")
    def test_invalid_ticker_format(self, mock_stock):
        """Should reject invalid ticker format."""
        result = get_etf_ohlcv_by_date("695", "20240101", "20240105")

        mock_stock.get_etf_ohlcv_by_date.assert_not_called()
        assert "error" in result
        assert "6-digit" in result["error"]

    @patch("pykrx_mcp.tools.etf_price.stock")
    def test_empty_dataframe(self, mock_stock):
        """Should handle empty DataFrame."""
        mock_stock.get_etf_ohlcv_by_date.return_value = pd.DataFrame()

        result = get_etf_ohlcv_by_date("999999", "20240101", "20240105")

        assert "error" in result
        assert "No ETF data found" in result["error"]


class TestGetEtfTickerList:
    """Test ETF ticker list retrieval."""

    @patch("pykrx_mcp.tools.etf_price.stock")
    def test_valid_request(self, mock_etf):
        """Should return ETF ticker list for valid request."""
        mock_etf.get_etf_ticker_list.return_value = [
            "069500",
            "114800",
            "252670",
        ]

        result = get_etf_ticker_list("20240101")

        mock_etf.get_etf_ticker_list.assert_called_once_with("20240101")
        assert result["date"] == "20240101"
        assert result["count"] == 3
        assert "069500" in result["tickers"]

    @patch("pykrx_mcp.tools.etf_price.stock")
    def test_invalid_date_format(self, mock_stock):
        """Should reject invalid date format."""
        result = get_etf_ticker_list("2024-01-01")

        mock_stock.get_etf_ticker_list.assert_not_called()
        assert "error" in result
        assert "YYYYMMDD" in result["error"]

    @patch("pykrx_mcp.tools.etf_price.stock")
    def test_empty_ticker_list(self, mock_stock):
        """Should handle empty ticker list."""
        mock_stock.get_etf_ticker_list.return_value = []

        result = get_etf_ticker_list("20240101")

        assert "error" in result
        assert "No ETFs found" in result["error"]
