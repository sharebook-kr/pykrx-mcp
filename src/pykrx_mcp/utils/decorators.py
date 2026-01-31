"""Decorators for MCP tool error handling."""

import logging
from collections.abc import Callable
from functools import wraps
from typing import Any

logger = logging.getLogger(__name__)


def mcp_tool_error_handler(func: Callable) -> Callable:
    """
    Decorator for MCP tools to provide consistent error handling.

    Responsibilities:
    - Automatic logging of function calls and results
    - Convert exceptions to MCP-compatible dict responses
    - Include input parameters in error responses for debugging

    pykrx handles domain-specific errors (invalid dates, missing data, etc.)
    This decorator only ensures MCP protocol compliance (dict responses).

    Args:
        func: The MCP tool function to wrap

    Returns:
        Wrapped function that returns dict on success or error
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> dict:
        func_name = func.__name__
        logger.info(f"[{func_name}] Called with kwargs={kwargs}")

        try:
            result = func(*args, **kwargs)

            # Count data rows if available for logging
            if isinstance(result, dict) and "data" in result:
                data = result["data"]
                row_count = len(data) if isinstance(data, list) else "N/A"
                logger.info(f"[{func_name}] Success - returned {row_count} rows")
            else:
                logger.info(f"[{func_name}] Success")

            return result

        except Exception as e:
            # pykrx errors are wrapped into MCP response format
            logger.error(f"[{func_name}] Error: {str(e)}")
            return {
                "error": str(e),
                "function": func_name,
                **kwargs,  # Include all input parameters for debugging
            }

    return wrapper
