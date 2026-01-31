# pykrx-mcp Development Guide

## 📋 프로젝트 개요

pykrx-mcp는 한국 주식 시장 데이터 라이브러리 `pykrx`를 MCP (Model Context Protocol) 서버로 제공하는 프로젝트입니다. AI 에이전트(Claude, GPT 등)가 한국 주식 데이터를 조회하고 분석할 수 있도록 설계되었습니다.

---

## 🏗️ 아키텍처 설계

### Phase 1: 모듈화 및 패턴 적용 (✅ 완료)

#### 디렉토리 구조

```
src/pykrx_mcp/
├── __about__.py              # 버전 관리 (단일 진실 공급원)
├── __init__.py
├── server.py                 # MCP 서버 orchestration (150줄)
│
├── resources/                # MCP Resources (AI가 읽는 정적 문서)
│   ├── __init__.py
│   ├── info.py              # KRX 기본 정보
│   └── manual.py            # pykrx 사용 가이드
│
├── tools/                    # MCP Tools (비즈니스 로직)
│   ├── __init__.py
│   ├── stock_price.py       # ✅ OHLCV 조회
│   ├── ticker_info.py       # ✅ 종목 리스트/이름 변환
│   ├── fundamental.py       # ✅ 기본 지표 (PER, PBR, EPS 등)
│   └── etf_price.py         # ✅ ETF OHLCV 및 종목 리스트
│
└── utils/                    # 재사용 가능한 헬퍼
    ├── __init__.py
    ├── decorators.py         # @mcp_tool_error_handler
    ├── validators.py         # validate_date/ticker_format
    └── formatters.py         # format_dataframe/error_response
```

#### Phase 1에 구현된 6개 핵심 도구

1. **`get_stock_ohlcv`** - 주식 OHLCV 데이터 조회 (100% coverage)
2. **`get_market_ticker_list`** - 시장별 종목 리스트 (100% coverage)
3. **`get_market_ticker_name`** - 종목코드 → 이름 변환 (100% coverage)
4. **`get_market_fundamental_by_date`** - 기본 지표 조회 (95% coverage)
5. **`get_etf_ohlcv_by_date`** - ETF OHLCV 데이터 (93% coverage)
6. **`get_etf_ticker_list`** - ETF 종목 리스트 (93% coverage)

#### 설계 원칙

1. **관심사의 분리 (Separation of Concerns)**
   - `server.py`: MCP 프로토콜 라우팅만 담당
   - `resources/`: 정적 문서 제공
   - `tools/`: 비즈니스 로직 구현
   - `utils/`: 공통 기능 추상화

2. **단일 책임 원칙 (Single Responsibility)**
   - 각 모듈은 하나의 명확한 역할만 수행
   - MCP 레이어와 도메인 로직 명확히 분리

3. **DRY (Don't Repeat Yourself)**
   - Decorator 패턴으로 반복 코드 제거
   - 헬퍼 함수로 공통 로직 재사용

---

## 🎯 적용된 디자인 패턴

### 1. Decorator Pattern - 에러 핸들링

**목적**: MCP 프로토콜 준수를 위한 자동 에러 처리

**구현**: `utils/decorators.py`

```python
@mcp_tool_error_handler
def get_stock_ohlcv(ticker: str, start_date: str, end_date: str):
    # 비즈니스 로직만 집중, try/except 불필요
    df = stock.get_market_ohlcv_by_date(...)
    return format_dataframe_response(df, ...)
```

**책임**:
- 자동 로깅 (`logger.info/error`)
- 예외를 MCP dict 응답으로 변환
- 입력 파라미터를 에러 응답에 자동 포함

**효과**: 23줄 → 7줄 (70% 감소)

---

### 2. Validator Pattern - 입력 검증

**목적**: MCP 레이어 특화 검증만 수행

**구현**: `utils/validators.py`

```python
def validate_date_format(date_str: str) -> tuple[bool, str]:
    """YYYYMMDD 형식만 검증 (날짜 유효성은 pykrx가 체크)"""
    if len(date_str) != 8 or not date_str.isdigit():
        return False, "Date must be YYYYMMDD format"
    return True, ""
```

**책임 분리**:

| 검증 항목 | MCP 레이어 | pykrx 레이어 |
|---------|-----------|-------------|
| 날짜 형식 (YYYYMMDD) | ✅ | - |
| 티커 형식 (6자리) | ✅ | - |
| 날짜 유효성 | - | ✅ |
| 티커 존재 여부 | - | ✅ |
| 거래일 체크 | - | ✅ |

---

### 3. Formatter Pattern - 응답 정규화

**목적**: 일관된 MCP 응답 구조 제공

**구현**: `utils/formatters.py`

```python
# 성공 응답
format_dataframe_response(df, ticker="005930", start_date="20240101")
# → {"ticker": "005930", "row_count": 20, "data": [...]}

# 에러 응답
format_error_response("No data", ticker="999999")
# → {"error": "No data", "ticker": "999999"}
```

---

## 🧪 테스트 전략

### 테스트 통계 (Phase 1 완료)

- **총 테스트**: 48개
- **통과율**: 100% (48/48)
- **전체 커버리지**: 77%

#### 모듈별 커버리지

| 모듈 | 라인 수 | 커버리지 | 비고 |
|-----|--------|---------|------|
| `utils/decorators.py` | 22 | 100% | ✅ |
| `utils/validators.py` | 20 | 100% | ✅ |
| `utils/formatters.py` | 6 | 100% | ✅ |
| `tools/stock_price.py` | 19 | 100% | ✅ |
| `tools/ticker_info.py` | 26 | 100% | ✅ |
| `tools/fundamental.py` | 19 | 95% | ✅ |
| `tools/etf_price.py` | 29 | 93% | ✅ |
| `server.py` | 35 | 0% | MCP 런타임 필요 |
| `resources/*` | 4 | 0% | 정적 문서 |

### 테스트 피라미드

```
        E2E (MCP Inspector)
              /\
             /  \
            /    \
      Integration  (선택)
          /        \
         /          \
    Unit Tests (필수) - 48개
   - validators  (15개)
   - formatters  (7개)
   - stock_price (7개)
   - ticker_info (8개)
   - fundamental (5개)
   - etf_price   (6개)
```

### 테스트 작성 가이드

```python
# tests/test_validators.py
class TestValidateDateFormat:
    def test_valid_date(self):
        assert validate_date_format("20240101") == (True, "")

    def test_invalid_format_with_hyphens(self):
        valid, msg = validate_date_format("2024-01-01")
        assert not valid
        assert "YYYYMMDD" in msg

# tests/test_stock_price.py (pykrx mock 사용)
@patch("pykrx_mcp.tools.stock_price.stock")
def test_valid_request(mock_stock):
    mock_df = pd.DataFrame({"종가": [70000, 71000]})
    mock_stock.get_market_ohlcv_by_date.return_value = mock_df

    result = get_stock_ohlcv("005930", "20240101", "20240105")
    assert result["row_count"] == 2
```

---

## 🔄 CI/CD 파이프라인

### GitHub Actions Workflow

**`.github/workflows/ci.yml`**

```yaml
jobs:
  test:
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]
    steps:
      - Install uv
      - Run pytest with coverage
      - Upload to Codecov

  lint:
    - ruff check
    - ruff format --check
```

**트리거**:
- PR 생성/업데이트 시
- `main` 브랜치 push 시

---

## 📦 새로운 Tool 추가 가이드

### Phase 2 예정 Tools

1. `get_market_cap_by_date` - 시가총액, 상장주식수
2. `get_market_net_purchases_by_date` - 투자자별 순매수
3. `get_market_trading_value_by_date` - 거래대금 조회
4. `get_index_ohlcv` - 지수 OHLCV 조회
5. Universal Query Executor - 범용 쿼리 실행기

### Tool 추가 절차 (Phase 1 완성 패턴 기반)

#### 1. `tools/` 디렉토리에 새 파일 생성

```python
# tools/market_cap.py

from pykrx import stock
from ..utils import (
    mcp_tool_error_handler,
    format_dataframe_response,
    validate_date_format,
    validate_ticker_format,
)

@mcp_tool_error_handler
def get_market_cap_by_date(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieve market capitalization data.

    Args:
        ticker: 6-digit stock ticker (e.g., "005930")
        start_date: Start date in YYYYMMDD format
        end_date: End date in YYYYMMDD format

    Returns:
        Dictionary with market cap, shares outstanding, etc.
    """
    # MCP 레벨 검증
    valid, msg = validate_ticker_format(ticker)
    if not valid:
        return {"error": msg, "ticker": ticker}

    valid, msg = validate_date_format(start_date)
    if not valid:
        return {"error": msg, "date": start_date}

    # pykrx 호출
    df = stock.get_market_cap_by_date(start_date, end_date, ticker)

    if df.empty:
        return format_error_response(
            f"No market cap data found for {ticker}",
            ticker=ticker, start_date=start_date, end_date=end_date
        )

    return format_dataframe_response(
        df, ticker=ticker, start_date=start_date, end_date=end_date
    )
    }
```

#### 2. `tools/__init__.py` 업데이트

```python
from .stock_price import get_stock_ohlcv
from .ticker_info import get_market_ticker_list

__all__ = [
    "get_stock_ohlcv",
    "get_market_ticker_list",
]
```

#### 3. `server.py`에 Tool 등록

```python
from .tools import get_stock_ohlcv_impl, get_market_ticker_list_impl

@mcp.tool()
def get_market_ticker_list(date: str, market: str = "KOSPI") -> dict:
    """
    Retrieve list of stock tickers for a specific market.
    ... (docstring은 AI가 읽음)
    """
    return get_market_ticker_list_impl(date, market)
```

#### 4. 테스트 작성

```python
# tests/test_ticker_info.py

@patch("pykrx_mcp.tools.ticker_info.stock")
def test_get_market_ticker_list(mock_stock):
    mock_stock.get_market_ticker_list.return_value = ["005930", "000660"]

    result = get_market_ticker_list("20240101", "KOSPI")

    assert result["count"] == 2
    assert "005930" in result["tickers"]
```

---

## 🚀 Phase 3: Universal Query Executor (향후)

### 개념

방대한 pykrx 기능을 모두 Explicit Tool로 만들지 않고, 범용 실행기로 제공

```python
@mcp.tool()
def execute_pykrx_query(
    module: str,      # "stock", "bond", "etf"
    function: str,    # "get_market_price_change_by_ticker"
    parameters: dict  # {"fromdate": "20240101", ...}
) -> dict:
    """
    Execute any pykrx function dynamically.

    Use this for advanced queries not covered by explicit tools.
    """
    # Allowlist 체크
    if function not in ALLOWED_FUNCTIONS:
        return {"error": f"Function {function} not allowed"}

    # 동적 실행
    pykrx_module = getattr(pykrx, module)
    pykrx_func = getattr(pykrx_module, function)

    result = pykrx_func(**parameters)
    return format_dataframe_response(result, **parameters)
```

### 안전 장치

1. **Allowlist**: 실행 가능한 함수 화이트리스트
2. **Parameter Validation**: 위험한 입력 필터링
3. **Rate Limiting**: 과도한 호출 방지

---

## 🔧 개발 환경 설정

### 필수 도구

```bash
# uv 설치 (패키지 관리자)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 개발 의존성 설치
uv sync --dev

# Editable 모드 설치
uv pip install -e .
```

### 개발 워크플로우

```bash
# 1. 코드 변경
vim src/pykrx_mcp/tools/new_tool.py

# 2. 테스트 작성
vim tests/test_new_tool.py

# 3. 테스트 실행
uv run pytest tests/test_new_tool.py -v

# 4. 전체 테스트 + 커버리지
uv run pytest tests/ --cov=src/pykrx_mcp --cov-report=term

# 5. Lint 체크
uv run ruff check src/ tests/
uv run ruff format src/ tests/

# 6. MCP Inspector로 수동 테스트
npm run inspector
```

---

## 📊 성능 메트릭

### 코드 효율성

| 항목 | 기존 | 현재 | 개선율 |
|------|------|------|--------|
| Tool 1개 코드 | 23줄 | 7줄 | 70% |
| Tool 15개 예상 | 345줄 | 155줄 | 55% |
| server.py | 239줄 | 88줄 | 63% |

### 테스트 실행 속도

- Unit Tests: ~0.6초 (29개)
- Coverage 포함: ~0.7초

---

## 🛡️ 에러 처리 철학

### MCP 레이어 vs pykrx 레이어

```
┌─────────────────────────────────────┐
│  MCP Layer (우리 책임)              │
│  - 형식 검증 (YYYYMMDD, 6자리)      │
│  - 프로토콜 준수 (dict 응답)        │
│  - 에러 메시지 AI 친화적 작성       │
└─────────────────────────────────────┘
              ↓
┌─────────────────────────────────────┐
│  pykrx Layer (pykrx 책임)           │
│  - 날짜 유효성 (실제 존재하는 날짜) │
│  - 티커 존재 여부                   │
│  - 거래일 체크                      │
│  - 데이터 조회                      │
└─────────────────────────────────────┘
```

### AI 친화적 에러 메시지

```python
# ❌ 나쁜 예
"Invalid input"

# ✅ 좋은 예
"Date must be YYYYMMDD format (e.g., '20240101'), got: '2024-01-01'"
```

---

## 📚 참고 자료

### MCP 관련

- [MCP 공식 문서](https://modelcontextprotocol.io)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Anthropic MCP 서버 예제](https://github.com/anthropics/anthropic-quickstarts/tree/main/mcp)

### pykrx 관련

- [pykrx GitHub](https://github.com/sharebook-kr/pykrx)
- [pykrx 문서](https://github.com/sharebook-kr/pykrx/wiki)

---

## 🤝 기여 가이드

### PR 체크리스트

- [ ] 새로운 Tool은 `@mcp_tool_error_handler` 사용
- [ ] Validator로 입력 형식 검증
- [ ] Formatter로 응답 정규화
- [ ] 유닛 테스트 작성 (최소 5개)
- [ ] Docstring 작성 (AI가 읽음)
- [ ] `ruff check` 통과
- [ ] 전체 테스트 통과

### 커밋 메시지 규칙

```
feat: Add get_market_ticker_list tool
fix: Correct date validation for leap years
test: Add edge cases for ticker format
refactor: Extract common validation logic
docs: Update tool usage examples
```

---

## 📅 로드맵

### ✅ Phase 1 (완료)
- 모듈 구조 리팩토링
- 디자인 패턴 적용
- 테스트 인프라 구축
- CI/CD 파이프라인

### 🚧 Phase 2 (다음 단계)
- 핵심 Tool 5-7개 추가
- Resource 문서 보강
- README 예제 추가

### 📋 Phase 3 (향후)
- Universal Query Executor
- Rate Limiting
- 캐싱 전략
- 성능 최적화

---

**Last Updated**: 2026-01-31
**Maintainer**: sharebook-kr
**License**: MIT
