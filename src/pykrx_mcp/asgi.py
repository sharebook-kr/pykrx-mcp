"""
ASGI application entry point for pykrx-mcp SSE server.

This module provides an ASGI-compatible app for deployment on cloud platforms
that use standard ASGI servers (uvicorn, gunicorn, etc.).
"""

import os

# Set SSE transport mode
os.environ["MCP_TRANSPORT"] = "sse"

# Import server and get the ASGI app
from pykrx_mcp.server import mcp

# FastMCP provides an SSE app via .sse_app property
# This is what uvicorn will serve
app = mcp.sse_app
