"""Stock analysis prompt with automatic ticker lookup."""

from datetime import datetime, timedelta

from .stock_data import MAJOR_STOCKS, PERIOD_MAPPING


def analyze_stock_by_name(
    stock_name: str, period: str = "1M", analysis_type: str = "price"
) -> str:
    """
    Analyze Korean stock by company name (handles ticker lookup automatically).

    This prompt helps AI understand the workflow to analyze stocks when users
    provide company names instead of ticker codes.

    Args:
        stock_name: Company name in Korean or English (e.g., "삼성전자", "NAVER")
        period: Analysis period - "1W", "1M", "3M", "6M", "1Y", etc. (default: "1M")
        analysis_type: Type of analysis - "price", "fundamental",
            "investor" (default: "price")

    Returns:
        Formatted prompt string for the AI model
    """
    # 주요 종목 매핑 확인
    ticker = MAJOR_STOCKS.get(stock_name)

    # 기간 계산 (대략적)
    days = PERIOD_MAPPING.get(period, 30)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    # 주요 종목인 경우
    if ticker:
        if analysis_type == "price":
            return f"""다음 단계로 {stock_name}의 주가를 분석해주세요:

**종목 정보 (자동 확인됨)**
- 종목명: {stock_name}
- Ticker: {ticker}
- 분석 기간: {period} (최근 {days}일)

**실행 단계**

1. **주가 데이터 조회**
   ```
   get_stock_ohlcv("{ticker}", "{start_str}", "{end_str}")
   ```

2. **데이터 분석**
   - 기간 내 최고가/최저가
   - 수익률 계산 (기간 시작 대비)
   - 평균 거래량
   - 주요 변동 시점 식별

3. **시각화**
   - 캔들스틱 차트 또는 라인 차트 생성
   - 거래량 바 차트 오버레이
   - 이동평균선 추가 (5일, 20일, 60일)

4. **인사이트 제공**
   - 추세 판단 (상승/하락/횡보)
   - 변동성 평가
   - 거래량 패턴 분석
"""
        elif analysis_type == "fundamental":
            return f"""다음 단계로 {stock_name}의 기본 지표를 분석해주세요:

**종목 정보**
- 종목명: {stock_name}
- Ticker: {ticker}

**실행 단계**

1. **기본 지표 조회**
   ```
   get_market_fundamental_by_date("{ticker}", "{start_str}", "{end_str}")
   ```

2. **주요 지표 분석**
   - PER (주가수익비율) 추이
   - PBR (주가순자산비율) 추이
   - EPS (주당순이익) 변화
   - DIV (배당수익률) 확인

3. **섹터 평균과 비교**
   - 같은 섹터 다른 종목들과 밸류에이션 비교
   - 역사적 평균 대비 현재 수준 평가

4. **투자 의견 제시**
   - 저평가/적정가/고평가 판단
   - 주의사항 및 리스크
"""
        else:  # investor
            return f"""다음 단계로 {stock_name}의 투자자별 수급을 분석해주세요:

**종목 정보**
- 종목명: {stock_name}
- Ticker: {ticker}
- 분석 기간: {period}

**실행 단계**

1. **수급 데이터 조회**
   ```
   # 투자자별 순매수 데이터 (외국인, 기관, 개인)
   get_market_net_purchases_of_equities_by_ticker(
       "{start_str}", "{end_str}", "{ticker}")
   ```

2. **주가와 함께 분석**
   ```
   get_stock_ohlcv("{ticker}", "{start_str}", "{end_str}")
   ```

3. **패턴 분석**
   - 외국인 순매수/순매도 누적액
   - 기관 매매 동향
   - 개인 투자자 패턴
   - 주가와의 상관관계

4. **시각화**
   - 이중 축 차트 (주가 + 누적 순매수)
   - 투자자별 막대 차트
"""

    # 주요 종목이 아닌 경우 (ticker를 모르는 경우)
    else:
        return f"""다음 단계로 {stock_name}의 주가를 분석해주세요:

**종목 정보 (ticker 코드 모름)**
- 종목명: {stock_name}
- 분석 기간: {period} (최근 {days}일)

**2단계 워크플로우**

### Step 1: Ticker 조회

먼저 KOSPI에서 검색:
```
get_market_ticker_list("{end_str}", "KOSPI")
```

결과에서 "{stock_name}" 검색:
- 반환된 ticker 목록에서 종목명 매칭
- `get_market_ticker_name(ticker)`로 각 ticker의 이름 확인
- "{stock_name}"과 일치하는 ticker 찾기

KOSPI에서 못 찾으면 KOSDAQ 시도:
```
get_market_ticker_list("{end_str}", "KOSDAQ")
```

### Step 2: Ticker를 찾은 후

찾은 ticker를 사용하여:
```
get_stock_ohlcv(ticker, "{start_str}", "{end_str}")
```

### Step 3: 데이터 분석 및 시각화

Step 1의 "주요 종목" 섹션과 동일하게 진행

---

**참고**: 다음번에는 더 빠른 조회를 위해 "{stock_name}"의 ticker 코드를 기억해두세요.

**주요 종목 빠른 참조**:
{_format_major_stocks()}
"""


def _format_major_stocks() -> str:
    """Format major stocks for display."""
    lines = []
    for name, ticker in list(MAJOR_STOCKS.items())[:10]:
        lines.append(f"- {name}: {ticker}")
    lines.append(f"... 외 {len(MAJOR_STOCKS) - 10}개")
    return "\n".join(lines)
