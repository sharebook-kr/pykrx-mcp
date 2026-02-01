"""
OpenAPI 스키마 검증 테스트.

REST API 구현(rest_api.py)의 모든 엔드포인트가 openapi.json에 정의되어 있는지 확인합니다.
"""

import json
import re
from pathlib import Path

import pytest


def extract_endpoints_from_rest_api():
    """rest_api.py 파일에서 모든 엔드포인트 추출."""
    rest_api_path = Path(__file__).parent.parent / "src" / "pykrx_mcp" / "rest_api.py"
    with open(rest_api_path, encoding="utf-8") as f:
        content = f.read()

    # @app.get(), @app.post() 등의 데코레이터에서 경로 추출
    pattern = r'@app\.(get|post|put|delete|patch)\("([^"]+)"'
    matches = re.findall(pattern, content)

    endpoints = {}
    for method, path in matches:
        if path not in endpoints:
            endpoints[path] = set()
        endpoints[path].add(method.upper())

    return endpoints


def load_openapi_spec():
    """openapi.json 파일 로드."""
    openapi_path = Path(__file__).parent.parent / "openapi.json"
    with open(openapi_path, encoding="utf-8") as f:
        return json.load(f)


def extract_endpoints_from_openapi(spec):
    """openapi.json에서 모든 엔드포인트 추출."""
    endpoints = {}
    for path, methods in spec.get("paths", {}).items():
        endpoints[path] = set()
        for method in methods.keys():
            if method in ["get", "post", "put", "delete", "patch"]:
                endpoints[path].add(method.upper())
    return endpoints


def test_all_rest_api_endpoints_in_openapi():
    """
    모든 REST API 엔드포인트가 openapi.json에 정의되어 있는지 확인.

    이 테스트는:
    1. rest_api.py의 모든 @app.METHOD() 데코레이터를 찾습니다
    2. openapi.json의 paths를 파싱합니다
    3. 누락된 엔드포인트가 있는지 확인합니다
    """
    rest_api_endpoints = extract_endpoints_from_rest_api()
    openapi_spec = load_openapi_spec()
    openapi_endpoints = extract_endpoints_from_openapi(openapi_spec)

    missing_endpoints = []
    method_mismatches = []

    for path, methods in rest_api_endpoints.items():
        if path not in openapi_endpoints:
            missing_endpoints.append(f"{path} (methods: {', '.join(methods)})")
        else:
            # 메서드도 일치하는지 확인
            openapi_methods = openapi_endpoints[path]
            missing_methods = methods - openapi_methods
            if missing_methods:
                method_mismatches.append(
                    f"{path}: {', '.join(missing_methods)} not in openapi.json"
                )

    # 검증 결과 출력
    if missing_endpoints:
        pytest.fail(
            "다음 엔드포인트가 openapi.json에 누락되었습니다:\n"
            + "\n".join(f"  - {ep}" for ep in missing_endpoints)
        )

    if method_mismatches:
        pytest.fail(
            "다음 HTTP 메서드가 openapi.json에 누락되었습니다:\n"
            + "\n".join(f"  - {mm}" for mm in method_mismatches)
        )


def test_openapi_version_matches_package():
    """openapi.json의 버전이 패키지 버전과 일치하는지 확인."""
    openapi_spec = load_openapi_spec()
    about_path = Path(__file__).parent.parent / "src" / "pykrx_mcp" / "__about__.py"

    with open(about_path, encoding="utf-8") as f:
        content = f.read()

    version_match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    assert version_match, "Could not find __version__ in __about__.py"

    package_version = version_match.group(1)
    openapi_version = openapi_spec.get("info", {}).get("version")

    assert openapi_version == package_version, (
        f"버전 불일치: openapi.json={openapi_version}, __about__.py={package_version}"
    )


def test_openapi_has_no_hardcoded_server():
    """openapi.json에 하드코딩된 서버 URL이 없는지 확인."""
    openapi_spec = load_openapi_spec()
    servers = openapi_spec.get("servers", [])

    assert len(servers) == 0, (
        f"openapi.json에 하드코딩된 서버가 있습니다: {servers}. 사용자가 직접 서버 URL을 설정해야 합니다."
    )


def test_openapi_schema_structure():
    """openapi.json의 기본 구조가 올바른지 확인."""
    openapi_spec = load_openapi_spec()

    # 필수 필드 확인
    assert "openapi" in openapi_spec, "openapi 버전 필드가 없습니다"
    assert "info" in openapi_spec, "info 섹션이 없습니다"
    assert "paths" in openapi_spec, "paths 섹션이 없습니다"

    # info 필드 확인
    info = openapi_spec["info"]
    assert "title" in info, "title이 없습니다"
    assert "version" in info, "version이 없습니다"
    assert "description" in info, "description이 없습니다"

    # OpenAPI 버전 확인
    assert openapi_spec["openapi"].startswith("3."), "OpenAPI 3.x 버전이어야 합니다"


def test_all_tool_endpoints_present():
    """
    필수 도구 엔드포인트가 모두 openapi.json에 존재하는지 확인.

    Development Guide에 명시된 8개의 도구 엔드포인트를 확인합니다.
    """
    openapi_spec = load_openapi_spec()
    openapi_endpoints = extract_endpoints_from_openapi(openapi_spec)

    required_tool_endpoints = [
        "/tools/get_stock_ohlcv",
        "/tools/get_market_ticker_list",
        "/tools/get_market_ticker_name",
        "/tools/get_market_fundamental_by_date",
        "/tools/get_market_cap_by_date",
        "/tools/get_market_trading_value_by_date",
        "/tools/get_etf_ohlcv_by_date",
        "/tools/get_etf_ticker_list",
    ]

    missing = [ep for ep in required_tool_endpoints if ep not in openapi_endpoints]

    assert not missing, (
        "필수 도구 엔드포인트가 openapi.json에 누락되었습니다:\n"
        + "\n".join(f"  - {ep}" for ep in missing)
    )

    # 모든 도구 엔드포인트가 POST 메서드를 사용하는지 확인
    for endpoint in required_tool_endpoints:
        methods = openapi_endpoints.get(endpoint, set())
        assert "POST" in methods, f"{endpoint}는 POST 메서드를 지원해야 합니다"


if __name__ == "__main__":
    # 로컬에서 직접 실행 시 간단한 리포트 출력
    print("🔍 OpenAPI 스키마 검증 중...\n")

    try:
        test_openapi_schema_structure()
        print("✅ OpenAPI 스키마 구조 검증 통과")
    except AssertionError as e:
        print(f"❌ OpenAPI 스키마 구조 오류: {e}")

    try:
        test_openapi_version_matches_package()
        print("✅ 버전 일치 검증 통과")
    except AssertionError as e:
        print(f"❌ 버전 불일치: {e}")

    try:
        test_openapi_has_no_hardcoded_server()
        print("✅ 하드코딩된 서버 URL 없음 확인")
    except AssertionError as e:
        print(f"❌ 하드코딩된 서버 URL 발견: {e}")

    try:
        test_all_tool_endpoints_present()
        print("✅ 모든 필수 도구 엔드포인트 존재 확인")
    except AssertionError as e:
        print(f"❌ 필수 엔드포인트 누락: {e}")

    try:
        test_all_rest_api_endpoints_in_openapi()
        print("✅ REST API와 OpenAPI 스키마 일치 확인")
    except Exception as e:
        print(f"❌ REST API와 OpenAPI 스키마 불일치: {e}")

    print("\n✨ 모든 검증 완료!")
