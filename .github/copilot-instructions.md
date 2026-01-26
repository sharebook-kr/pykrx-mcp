# pykrx-mcp Development Guide

## Project Overview
This is an MCP (Model Context Protocol) server that exposes the `pykrx` Korean stock market data library to AI agents like Claude Desktop. The server runs via stdio and provides tools for querying KOSPI/KOSDAQ stock data.

## Architecture

**Core Components:**
- `src/pykrx_mcp/server.py`: FastMCP server with tool definitions
- `src/pykrx_mcp/__about__.py`: Single source of truth for version management
- `.github/workflows/publish.yml`: Dual-trigger automated release workflow

**MCP stdio Pattern:**
- All logging MUST go to `sys.stderr` (stdout is reserved for MCP protocol communication)
- Tool functions are decorated with `@mcp.tool()` and use type hints for LLM schema generation
- Entry point: `mcp.run()` in `main()` function

## Version Management

Version lives in `src/pykrx_mcp/__about__.py` as `__version__ = "x.y.z"`. This is:
- Read by hatchling build system via `[tool.hatch.version]` in pyproject.toml
- Auto-bumped by CI during pykrx dependency updates
- Manually updated for feature releases

## Automated Release Workflow

**Two release triggers:**

1. **`repository_dispatch` (pykrx_release)**: External signal from pykrx repository
   - Runs `update-version` job
   - Executes `uv lock --upgrade-package pykrx` to update dependency
   - Bumps patch version in `__about__.py`
   - Commits changes and creates git tag `vX.Y.Z`
   - Tag push triggers the publish job (see below)

2. **`push` tags (v*)**: Manual or automated tag push
   - Runs `publish` job with `environment: pypi`
   - Builds package with `uv build`
   - Publishes to PyPI using OIDC Trusted Publishing (no API keys)
   - Creates GitHub Release

**Key workflow details:**
- Jobs are split and conditionally triggered via `if: github.event_name == '...'`
- Version bumping uses shell script to parse and increment `__about__.py`
- Requires GitHub environment named `pypi` with OIDC setup

## Adding New Tools

When adding new MCP tools to `server.py`:

1. Use `@mcp.tool()` decorator
2. Include comprehensive docstrings (LLM reads these for tool discovery)
3. Use type hints on all parameters (generates JSON schema)
4. Document Korean stock market specifics (6-digit tickers, YYYYMMDD dates)
5. Return structured dictionaries with error fields
6. Log to stderr using the `logger` instance

**Example pattern:**
```python
@mcp.tool()
def get_market_data(ticker: str, date: str) -> dict:
    """
    Clear description of what this does and when to use it.
    
    Args:
        ticker: Specific format explanation (e.g., "6-digit code")
        date: Format details (e.g., "YYYYMMDD")
    
    Returns:
        Structure description
    """
    try:
        logger.info(f"Fetching {ticker}")
        result = stock.some_pykrx_function(ticker, date)
        return {"data": result.to_dict(orient='records')}
    except Exception as e:
        logger.error(f"Error: {e}")
        return {"error": str(e), "ticker": ticker}
```

## Development Workflow

**Setup:**
```bash
uv pip install -e .     # Editable install with uv
pykrx-mcp              # Run server (blocks on stdio)
```

**Testing MCP server:**
Use MCP inspector or configure in Claude Desktop config:
```json
{
  "mcpServers": {
    "pykrx": {"command": "uvx", "args": ["pykrx-mcp"]}
  }
}
```

## Release Process

**For pykrx dependency updates (automated):**
- Upstream `pykrx` repository sends `repository_dispatch` webhook
- CI handles everything automatically

**For feature releases (manual):**
1. Update `__about__.py` version (e.g., `0.1.0` → `0.2.0` for features)
2. Commit changes
3. Create and push tag: `git tag v0.2.0 && git push origin v0.2.0`
4. CI publishes to PyPI automatically

## Project Conventions

- **No version in pyproject.toml**: Uses `dynamic = ["version"]` with hatchling
- **Package structure**: `src/` layout for proper isolation
- **Entry point**: `[project.scripts]` defines `pykrx-mcp` command
- **Korean market specifics**: Tickers are 6-digit strings, dates are YYYYMMDD format
- **Error handling**: Return error dicts rather than raising (better for LLM consumption)
