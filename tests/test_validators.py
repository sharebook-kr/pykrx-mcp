"""Tests for input validators."""

from pykrx_mcp.utils.validators import validate_date_format, validate_ticker_format


class TestValidateDateFormat:
    """Test date format validation."""

    def test_valid_date(self):
        """Valid YYYYMMDD format should pass."""
        assert validate_date_format("20240101") == (True, "")
        assert validate_date_format("20231231") == (True, "")
        assert validate_date_format("19900101") == (True, "")

    def test_invalid_format_with_hyphens(self):
        """Date with hyphens should fail."""
        valid, msg = validate_date_format("2024-01-01")
        assert not valid
        assert "YYYYMMDD" in msg
        assert "2024-01-01" in msg

    def test_invalid_format_with_slashes(self):
        """Date with slashes should fail."""
        valid, msg = validate_date_format("01/01/2024")
        assert not valid
        assert "YYYYMMDD" in msg

    def test_invalid_length_too_short(self):
        """Date shorter than 8 digits should fail."""
        valid, msg = validate_date_format("240101")
        assert not valid
        assert "YYYYMMDD" in msg

    def test_invalid_length_too_long(self):
        """Date longer than 8 digits should fail."""
        valid, msg = validate_date_format("202401011")
        assert not valid
        assert "YYYYMMDD" in msg

    def test_invalid_non_numeric(self):
        """Date with non-numeric characters should fail."""
        valid, msg = validate_date_format("2024010a")
        assert not valid
        assert "YYYYMMDD" in msg

    def test_invalid_type_not_string(self):
        """Non-string input should fail."""
        valid, msg = validate_date_format(20240101)
        assert not valid
        assert "string" in msg

    def test_empty_string(self):
        """Empty string should fail."""
        valid, msg = validate_date_format("")
        assert not valid
        assert "YYYYMMDD" in msg


class TestValidateTickerFormat:
    """Test ticker format validation."""

    def test_valid_ticker(self):
        """Valid 6-digit tickers should pass."""
        assert validate_ticker_format("005930") == (True, "")
        assert validate_ticker_format("000660") == (True, "")
        assert validate_ticker_format("035420") == (True, "")

    def test_invalid_length_too_short(self):
        """Ticker shorter than 6 digits should fail."""
        valid, msg = validate_ticker_format("5930")
        assert not valid
        assert "6-digit" in msg
        assert "5930" in msg

    def test_invalid_length_too_long(self):
        """Ticker longer than 6 digits should fail."""
        valid, msg = validate_ticker_format("0059301")
        assert not valid
        assert "6-digit" in msg

    def test_invalid_non_numeric(self):
        """Ticker with non-numeric characters should fail."""
        valid, msg = validate_ticker_format("00593A")
        assert not valid
        assert "numeric" in msg

    def test_invalid_type_not_string(self):
        """Non-string input should fail."""
        valid, msg = validate_ticker_format(5930)
        assert not valid
        assert "string" in msg

    def test_empty_string(self):
        """Empty string should fail."""
        valid, msg = validate_ticker_format("")
        assert not valid
        assert "6-digit" in msg

    def test_with_leading_zeros_preserved(self):
        """Tickers with leading zeros should be preserved."""
        valid, _ = validate_ticker_format("000001")
        assert valid
