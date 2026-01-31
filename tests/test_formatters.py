"""Tests for response formatters."""

import pandas as pd

from pykrx_mcp.utils.formatters import (
    format_dataframe_response,
    format_error_response,
)


class TestFormatDataFrameResponse:
    """Test DataFrame response formatting."""

    def test_basic_dataframe(self):
        """Should convert DataFrame to dict with row count."""
        df = pd.DataFrame({"Close": [70000, 71000], "Volume": [1000, 1100]})
        result = format_dataframe_response(df, ticker="005930")

        assert "ticker" in result
        assert result["ticker"] == "005930"
        assert "row_count" in result
        assert result["row_count"] == 2
        assert "data" in result
        assert len(result["data"]) == 2

    def test_with_index(self):
        """Should reset index and include in data."""
        df = pd.DataFrame({"Close": [70000, 71000]}, index=["2024-01-01", "2024-01-02"])
        result = format_dataframe_response(df)

        assert result["row_count"] == 2
        assert "index" in result["data"][0]  # Index becomes a column

    def test_empty_dataframe(self):
        """Should handle empty DataFrame."""
        df = pd.DataFrame()
        result = format_dataframe_response(df, ticker="999999")

        assert result["row_count"] == 0
        assert result["data"] == []
        assert result["ticker"] == "999999"

    def test_multiple_metadata(self):
        """Should include all provided metadata."""
        df = pd.DataFrame({"Price": [100]})
        result = format_dataframe_response(
            df,
            ticker="005930",
            start_date="20240101",
            end_date="20240131",
            adjusted=True,
        )

        assert result["ticker"] == "005930"
        assert result["start_date"] == "20240101"
        assert result["end_date"] == "20240131"
        assert result["adjusted"] is True
        assert result["row_count"] == 1


class TestFormatErrorResponse:
    """Test error response formatting."""

    def test_basic_error(self):
        """Should create error dict with message."""
        result = format_error_response("Something went wrong")

        assert "error" in result
        assert result["error"] == "Something went wrong"

    def test_error_with_context(self):
        """Should include context parameters."""
        result = format_error_response(
            "No data found", ticker="999999", start_date="20240101"
        )

        assert result["error"] == "No data found"
        assert result["ticker"] == "999999"
        assert result["start_date"] == "20240101"

    def test_error_with_multiple_context(self):
        """Should include all context parameters."""
        result = format_error_response(
            "Invalid request",
            ticker="005930",
            start_date="20240101",
            end_date="20240131",
            reason="Bad format",
        )

        assert result["error"] == "Invalid request"
        assert result["ticker"] == "005930"
        assert result["start_date"] == "20240101"
        assert result["end_date"] == "20240131"
        assert result["reason"] == "Bad format"
