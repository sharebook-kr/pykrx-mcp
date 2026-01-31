"""Basic KRX market information resource."""


def get_krx_info() -> str:
    """General information about Korean stock market (KRX)."""
    return """
    # Korean Stock Exchange (KRX) Information

    The Korea Exchange (KRX) operates:
    - KOSPI: Korea Composite Stock Price Index (main board)
    - KOSDAQ: Korean Securities Dealers Automated Quotations (tech/growth stocks)

    Trading hours: 09:00-15:30 KST (Mon-Fri)
    Stock tickers: 6-digit codes (e.g., 005930 for Samsung Electronics)
    """
