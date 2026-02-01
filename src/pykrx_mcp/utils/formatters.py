"""Response formatters for MCP tools."""

from typing import Any

import pandas as pd


def dict_to_table(data: dict) -> str:
    """
    Convert dictionary data to a simple table format.

    Args:
        data: Dictionary to convert to table format

    Returns:
        String representation of table

    Example:
        >>> dict_to_table({"a": 1, "b": 2})
        "a: 1\\nb: 2"
    """
    if not data:
        return ""

    # Handle nested dictionary (e.g., date-indexed data)
    if isinstance(next(iter(data.values()), None), dict):
        lines = []
        for key, value in data.items():
            lines.append(f"{key}:")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        return "\n".join(lines)

    # Handle simple dictionary
    return "\n".join(f"{k}: {v}" for k, v in data.items())


def format_dataframe_response(df: pd.DataFrame, **metadata: Any) -> dict:
    """
    Convert pandas DataFrame to MCP-compatible dict response.

    Args:
        df: pandas DataFrame to convert
        **metadata: Additional metadata to include (ticker, dates, etc.)

    Returns:
        Dictionary with metadata and data records

    Example:
        >>> df = pd.DataFrame({'Close': [70000, 71000]})
        >>> format_dataframe_response(df, ticker="005930", start_date="20240101")
        {
            'ticker': '005930',
            'start_date': '20240101',
            'row_count': 2,
            'data': [{'Close': 70000}, {'Close': 71000}]
        }
    """
    # Reset index to make date column accessible
    df_copy = df.reset_index()

    # Convert datetime columns to string format (YYYY-MM-DD)
    for col in df_copy.columns:
        if pd.api.types.is_datetime64_any_dtype(df_copy[col]):
            df_copy[col] = df_copy[col].dt.strftime("%Y-%m-%d")

    return {
        **metadata,
        "row_count": len(df),
        "data": df_copy.to_dict(orient="records"),
    }


def format_error_response(message: str, **context: Any) -> dict:
    """
    Create consistent error response structure.

    Args:
        message: Error message
        **context: Additional context (ticker, dates, etc.)

    Returns:
        Dictionary with error and context

    Example:
        >>> format_error_response("No data found", ticker="999999")
        {'error': 'No data found', 'ticker': '999999'}
    """
    return {"error": message, **context}
