"""Investor flow analysis prompt."""

from datetime import datetime, timedelta

from .stock_data import MAJOR_STOCKS, PERIOD_MAPPING


def analyze_investor_flow(
    stock_name: str, period: str = "1M", focus_investor: str = "all"
) -> str:
    """
    Analyze investor trading patterns (foreign, institutional, individual).

    This prompt guides AI to analyze supply/demand dynamics by investor type.

    Args:
        stock_name: Company name in Korean (e.g., "삼성전자")
        period: Analysis period - "1W", "1M", "3M", "6M", "1Y" (default: "1M")
        focus_investor: Focus on specific investor - "foreign",
            "institution", "individual", "all" (default: "all")

    Returns:
        Formatted prompt string for investor flow analysis
    """
    # Ticker 매핑
    ticker = MAJOR_STOCKS.get(stock_name)

    # 기간 계산
    days = PERIOD_MAPPING.get(period, 30)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    # Investor 타입별 한글명
    investor_kr = {
        "foreign": "외국인",
        "institution": "기관",
        "individual": "개인",
        "all": "전체 투자자",
    }

    focus_kr = investor_kr.get(focus_investor, "전체 투자자")

    if ticker:
        workflow = f"""다음 단계로 {stock_name}의 {focus_kr} 수급을 분석해주세요:

**종목 정보**
- 종목명: {stock_name}
- Ticker: {ticker}
- 분석 기간: {period} (최근 {days}일)
- 집중 분석: {focus_kr}

**실행 단계**

### 1. 투자자별 매매 데이터 조회

**주의**: pykrx의 정확한 함수명을 확인하세요. 일반적으로:
```
# Option A: 투자자별 순매수 (기간별)
stock.get_market_net_purchases_of_equities_by_ticker(
    fromdate="{start_str}",
    todate="{end_str}",
    ticker="{ticker}"
)

# Option B: 일자별 투자자 거래
stock.get_market_trading_value_by_date(
    fromdate="{start_str}",
    todate="{end_str}",
    ticker="{ticker}"
)
```

### 2. 주가 데이터 함께 조회 (상관관계 분석용)
```
get_stock_ohlcv("{ticker}", "{start_str}", "{end_str}")
```

### 3. 데이터 분석

**외국인 투자자 (Foreign)**
- 순매수/순매도 누적액 계산
- 보유 비중 변화 (가능한 경우)
- 주가와의 상관관계 분석
- 패턴: 외국인이 사면 주가 상승하는 경향

**기관 투자자 (Institution)**
- 연기금, 보험사, 자산운용사 등
- 순매수 규모 및 지속성
- 기관 매수 = 펀더멘털 신뢰 신호

**개인 투자자 (Individual)**
- 개인 순매수/순매도 패턴
- 역추세 매매 경향 (떨어지면 사고, 오르면 팔고)
- 거래대금 비중

### 4. 시각화

**차트 1: 이중 축 차트**
- 왼쪽 축: 주가 (종가 라인)
- 오른쪽 축: 투자자별 누적 순매수 (라인 3개)
- X축: 날짜

**차트 2: 일별 순매수 막대 차트**
- X축: 날짜
- Y축: 순매수 금액 (억원)
- 투자자별로 색상 구분
- 양수 = 순매수, 음수 = 순매도

### 5. 인사이트 도출

**주요 질문에 답변:**
1. 최근 {period} 동안 누가 주도적으로 매수/매도했나?
2. 외국인과 기관의 매매 방향이 일치하는가?
3. 주가와 수급의 상관관계는?
4. 최근 수급 전환 시점이 있는가?

**투자 시사점:**
- 외국인+기관 동반 매수 → 강세 신호
- 개인 홀로 매수 → 주의 필요 (역추세 가능성)
- 수급 전환 시점 주목
"""
    else:
        workflow = f"""다음 단계로 {stock_name}의 {focus_kr} 수급을 분석해주세요:

**종목 정보 (ticker 모름)**
- 종목명: {stock_name}
- 분석 기간: {period}

**Step 1: Ticker 조회 먼저**

```
# KOSPI에서 검색
tickers = get_market_ticker_list("{end_str}", "KOSPI")

# 종목명으로 ticker 찾기
for ticker in tickers:
    name = get_market_ticker_name(ticker)
    if "{stock_name}" in name:
        # ticker 확인됨
        break
```

**Step 2: Ticker 확인 후**

위의 "주요 종목" 섹션 워크플로우를 동일하게 진행합니다.
"""

    return workflow
