# pykrx-mcp Development Guide

## Project Overview
This is an MCP (Model Context Protocol) server that exposes the `pykrx` Korean stock market data library to AI agents like Claude Desktop. The server runs via stdio and provides tools for querying KOSPI/KOSDAQ stock data.

## Architecture

**Core Components:**
- `src/pykrx_mcp/server.py`: FastMCP server with tool definitions
- `src/pykrx_mcp/__about__.py`: Single source of truth for version management
- `smithery.yaml`: Smithery registry metadata (auto-synced with Python version)
- `scripts/sync_smithery_version.py`: Version synchronization script
- `.github/workflows/publish.yml`: Fully automated dual-platform release workflow

**MCP stdio Pattern:**
- All logging MUST go to `sys.stderr` (stdout is reserved for MCP protocol communication)
- Tool functions are decorated with `@mcp.tool()` and use type hints for LLM schema generation
- Resources are decorated with `@mcp.resource()` to provide static documentation and guides
- Entry point: `mcp.run()` in `main()` function

## Version Management

**Single source of truth:** `src/pykrx_mcp/__about__.py`

```python
__version__ = "x.y.z"
```
Fully Automated Release Workflow

**Two automated paths to release:**

### Path 1: Upstream pykrx Update (Fully Automated)

**Trigger:** `repository_dispatch` event from pykrx repository

**What happens:**
1. CI upgrades pykrx dependency: `uv lock --upgrade-package pykrx`
2. Bumps patch version in `__about__.py` (e.g., `0.1.0` → `0.1.1`)
3. Runs `scripts/sync_smithery_version.py` to sync `smithery.yaml`
4. Commits: `uv.lock`, `__about__.py`, `smithery.yaml`
5. Creates git tag `v0.1.1`
6. Pushes commit and tag to main branch
7. Tag push triggers Path 2 (below)

**Zero manual intervention required.**

### Path 2: Tag Push (Fully Automated)

**Trigger:** Git tag push matching `v*` pattern

**What happens:**
1. Builds Python package: `uv build`
2. Publishes to PyPI via OIDC Trusted Publishing
3. Creates GitHub Release with auto-generated notes
4. Smithery auto-detects updated `smithery.yaml` from the tagged commit

**Works for both:**
- Tags created by Path 1 (automated)
- Tags created manually (see below)

### Manual Feature Release

**When you add new tools/resources:**

```bash
# 1. Update version in __about__.py
# Change: __version__ = "0.1.0"
# To:     __version__ = "0.2.0"  # for minor release

# 2. Commit changes
7. **Update version in `__about__.py`** (minor bump for new tools)
8. **Create and push tag** - CI handles the rest
git add src/pykrx_mcp/__about__.py
git commit -m "feat: add new tool for XYZ"

# 3. Create and push tag
git tag v0.2.0
git push origin main
git push origin v0.2.0

# 4. CI handles everything else automatically:
#    - Syncs smithery.yaml to version 0.2.0
#    - Publishes to PyPI
#    - Creates GitHub Release
#    - Smithery detects update
```

**That's it!** No need to manually edit `smithery.yaml`.

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

## Adding MCP Resources

MCP resources provide static documentation and usage guides that AI models can read before using tools. Resources dramatically improve model accuracy and reduce errors by providing context about constraints, formats, and best practices.

**When to add resources:**
- Documenting API constraints (date formats, ticker formats)
- Providing tool selection guidance (which tool for which task)
- Explaining rate limits and performance considerations
- Creating self-healing guides (common errors and fixes)

**Resource pattern:**
```python
@mcp.resource("krx://resource-name")
def get_resource_name() -> str:
    """Brief description of what this resource provides."""
    return """
    # Resource Title

    Comprehensive documentation that the AI model will read.
    Include:
   Version Sync Script

**Purpose:** `scripts/sync_smithery_version.py`
- Reads version from `__about__.py`
- Updates `version:` field in `smithery.yaml`
- Used by CI automatically, can also run locally

**Local testing:**
```bash
python scripts/sync_smithery_version.py
# Output: ✓ Updated smithery.yaml to version X.Y.Z
```

## Smithery Registration

**Installation via Smithery:**
```bash
smithery install pykrx-mcp
```

After updating `smithery.yaml`, Smithery automatically detects changes from tagged releases.

## Release Process

**For pykrx dependency updates (automated):**
- Upstream `pykrx` repository sends `repository_dispatch` webhook
- CI handles everything automatically: dependency update → version bump → PyPI + Smithery

**For feature releases (manual):**
1. Update `__about__.py` version (e.g., `0.1.0` → `0.2.0` for new features)
2. Commit changes: `git commit -am "feat: add new functionality"`
3. Create and push tag: `git tag v0.2.0 && git push origin main --tags`
4. CI automatically syncs `smithery.yaml`, publishes to PyPI, and updates GitHub Releaseth correct/incorrect examples
  - Tool selection guide (which tool for which user question)
  - Best practices for long-term data queries and rate limiting
  - Common error patterns and troubleshooting steps
  - Known limitations of the pykrx library

**Benefits of well-designed resources:**
- Models learn constraints before making tool calls (fewer format errors)
- Self-healing: Models refer back to guides when encountering errors
- Reduced hallucination: Clear documentation of what IS and ISN'T possible
- Better UX: AI provides more accurate responses on first attempt

## Development Workflow

**Setup:**
```bash
uv pip install -e .     # Editable install with uv
pykrx-mcp              # Run server (blocks on stdio)
```

**TeSingle version source**: `__about__.py` only (smithery.yaml auto-synced)
- **No manual smithery.yaml edits**: Let CI handle synchronization
- **Package structure**: `src/` layout for proper isolation
- **Entry point**: `[project.scripts]` defines `pykrx-mcp` command
- **Korean market specifics**: Tickers are 6-digit strings, dates are YYYYMMDD format
- **Error handling**: Return error dicts rather than raising (better for LLM consumption)
- **Automated releases**: Tag push = PyPI + Smithery deployment
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
