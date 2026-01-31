"""Sync smithery.yaml version with Python package version."""

import re
import sys
from pathlib import Path


def get_python_version() -> str:
    """Read version from __about__.py"""
    about_file = Path(__file__).parent.parent / "src" / "pykrx_mcp" / "__about__.py"
    content = about_file.read_text()
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("Could not find __version__ in __about__.py")
    return match.group(1)


def update_smithery_version(new_version: str) -> None:
    """Update version in smithery.yaml"""
    smithery_file = Path(__file__).parent.parent / "smithery.yaml"
    content = smithery_file.read_text()

    # smithery.yaml의 version 필드 업데이트 (콜론 형식)
    updated = re.sub(
        r"^version:\s*[\d.]+", f"version: {new_version}", content, flags=re.MULTILINE
    )

    if updated == content:
        raise ValueError("Failed to update version in smithery.yaml")

    smithery_file.write_text(updated)
    print(f"✓ Updated smithery.yaml to version {new_version}")


def main():
    try:
        python_version = get_python_version()
        update_smithery_version(python_version)
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
