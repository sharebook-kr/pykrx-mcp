"""Sync smithery.yaml and server.json versions with Python package version."""

import json
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

    # 현재 버전 확인
    current_match = re.search(r"^version:\s*([\d.]+)", content, flags=re.MULTILINE)
    if current_match:
        current_version = current_match.group(1)
        if current_version == new_version:
            print(f"✓ smithery.yaml already at version {new_version}")
            return

    # smithery.yaml의 version 필드 업데이트
    updated = re.sub(
        r"^version:\s*[\d.]+.*$",
        f"version: {new_version}",
        content,
        flags=re.MULTILINE,
    )

    if updated == content:
        raise ValueError("Failed to update version in smithery.yaml")

    smithery_file.write_text(updated)
    print(f"✓ Updated smithery.yaml to version {new_version}")


def update_server_json_version(new_version: str) -> None:
    """Update version in server.json"""
    server_json_file = Path(__file__).parent.parent / "server.json"

    with open(server_json_file) as f:
        data = json.load(f)

    # 현재 버전 확인
    current_version = data.get("version")
    if current_version == new_version:
        packages_version = (
            data.get("packages", [{}])[0].get("version")
            if data.get("packages")
            else None
        )
        if packages_version == new_version:
            print(f"✓ server.json already at version {new_version}")
            return

    # Top-level version 업데이트
    data["version"] = new_version

    # packages[0].version 업데이트
    if "packages" in data and len(data["packages"]) > 0:
        data["packages"][0]["version"] = new_version

    with open(server_json_file, "w") as f:
        json.dump(data, f, indent=2)
        f.write("\n")  # 마지막 줄바꿈 추가

    print(f"✓ Updated server.json to version {new_version}")


def main():
    try:
        python_version = get_python_version()
        update_smithery_version(python_version)
        update_server_json_version(python_version)
        return 0
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
