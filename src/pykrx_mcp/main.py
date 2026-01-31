"""
Render deployment entry point for pykrx-mcp SSE server.

This module provides a simple entry point for deploying pykrx-mcp
as an HTTP/SSE server on cloud platforms like Render.

FastMCP uses uvicorn internally, which reads HOST and PORT from environment.
"""

import os


def main():
    """
    Entry point for Render deployment.
    Configures environment and delegates to server.main().
    """
    # Set transport to SSE for cloud deployment
    os.environ["MCP_TRANSPORT"] = "sse"

    # FastMCP's SSE mode uses uvicorn, which reads these env vars:
    # - HOST: bind address (default: 127.0.0.1)
    # - PORT: bind port (default: 8000)

    # Set defaults for cloud deployment
    if "HOST" not in os.environ:
        os.environ["HOST"] = "0.0.0.0"  # Listen on all interfaces

    # Render provides PORT automatically, but set default for local testing
    if "PORT" not in os.environ:
        os.environ["PORT"] = "8000"

    # Import and run the main server
    from pykrx_mcp.server import main as server_main

    server_main()


if __name__ == "__main__":
    main()
