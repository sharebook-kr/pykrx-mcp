"""Stock screening prompt for finding undervalued stocks."""

from datetime import datetime


def screen_undervalued_stocks(
    max_per: float = 10.0,
    max_pbr: float = 1.0,
    market: str = "KOSPI",
    min_market_cap: int = 1000,
    sort_by: str = "PER",
) -> str:
    """
    Screen for potentially undervalued stocks based on fundamental metrics.

    This prompt guides AI through a multi-step screening workflow.

    Args:
        max_per: Maximum PER (Price-to-Earnings Ratio) threshold (default: 10.0)
        max_pbr: Maximum PBR (Price-to-Book Ratio) threshold (default: 1.0)
        market: Target market - "KOSPI", "KOSDAQ", or "ALL" (default: "KOSPI")
        min_market_cap: Minimum market cap in billions KRW (default: 1000 = 1조원)
        sort_by: Sort results by - "PER", "PBR", "MarketCap", "EPS" (default: "PER")

    Returns:
        Formatted prompt string for stock screening
    """
    today = datetime.now().strftime("%Y%m%d")

    return f"""다음 조건으로 저평가 종목을 스크리닝해주세요:

**스크리닝 조건**
- PER (주가수익비율) ≤ {max_per}
- PBR (주가순자산비율) ≤ {max_pbr}
- 시장: {market}
- 최소 시가총액: {min_market_cap:,}억원
- 정렬 기준: {sort_by}

**실행 단계**

### Step 1: 전체 종목 리스트 조회

{"KOSPI와 KOSDAQ 모두 조회:" if market == "ALL" else f"{market} 종목만 조회:"}

```python
# {"KOSPI 종목" if market != "ALL" else "KOSPI + KOSDAQ 종목"}
kospi_tickers = get_market_ticker_list("{today}", "KOSPI")
{"kosdaq_tickers = get_market_ticker_list('" + today + "', " if market == "ALL" else ""}
{"    'KOSDAQ')" if market == "ALL" else ""}
{"all_tickers = list(kospi_tickers) + list(kosdaq_tickers)" if market == "ALL" else ""}
```

### Step 2: 기본 지표 데이터 조회

**주의**: 전체 종목을 한 번에 조회할 수 없으므로, 날짜 기준으로 조회:

```python
# 특정 날짜의 전체 시장 기본 지표
fundamental_data = get_market_fundamental_by_date(
    date="{today}",
    market="{market if market != "ALL" else "KOSPI"}"
)

{"# KOSDAQ도 조회 (market='ALL'인 경우)" if market == "ALL" else ""}
{"fundamental_kosdaq = get_market_fundamental_by_date(" if market == "ALL" else ""}
{"    date='" + today + "', market='KOSDAQ')" if market == "ALL" else ""}
{"fundamental_data = pd.concat([fundamental_data, " if market == "ALL" else ""}
{"    fundamental_kosdaq])" if market == "ALL" else ""}
```

### Step 3: 시가총액 데이터 조회 (필터링용)

```python
# 시가총액은 별도 조회가 필요할 수 있음
# get_market_cap_by_date는 개별 종목용이므로,
# fundamental 데이터에 시가총액이 포함되어 있는지 확인

# 만약 포함되어 있지 않다면:
# 각 종목의 시가총액을 순회하며 조회 (시간 소요)
```

### Step 4: 필터링

DataFrame을 활용한 필터링:

```python
# 1. PER 필터
filtered = fundamental_data[fundamental_data['PER'] <= {max_per}]

# 2. PBR 필터
filtered = filtered[filtered['PBR'] <= {max_pbr}]

# 3. 시가총액 필터 (단위 확인 필요)
# 만약 시가총액이 '억원' 단위라면:
filtered = filtered[filtered['시가총액'] >= {min_market_cap}]

# 4. 음수 제거 (적자 기업 제외)
filtered = filtered[filtered['PER'] > 0]
filtered = filtered[filtered['PBR'] > 0]
filtered = filtered[filtered['EPS'] > 0]
```

### Step 5: 정렬 및 상위 종목 추출

```python
# {sort_by} 기준 오름차순 정렬
sorted_stocks = filtered.sort_values(by='{sort_by}', ascending=True)

# 상위 30개 추출
top_30 = sorted_stocks.head(30)
```

### Step 6: 종목명 추가 (가독성 향상)

```python
# Ticker 코드를 종목명으로 변환
top_30['종목명'] = top_30.index.map(lambda t: get_market_ticker_name(t)['name'])
```

### Step 7: 결과 시각화

**표 형식 출력:**
```
순위 | 종목명 | Ticker | PER | PBR | EPS | 시가총액
-----|--------|--------|-----|-----|-----|----------
1    | ...    | ...    | ... | ... | ... | ...
```

**차트 시각화:**
- X축: 종목명 (상위 10개)
- Y축: PER 또는 PBR
- 막대 차트 또는 산점도

### Step 8: 추가 분석 (선택사항)

**상위 종목의 최근 주가 추이:**
```python
# 1위 종목의 최근 1개월 주가
top_ticker = top_30.index[0]
get_stock_ohlcv(top_ticker, "20260101", "{today}")
```

**섹터별 분포:**
- 저PER 종목들이 특정 섹터에 몰려있는지 확인
- 경기민감주 vs 경기방어주

### 주의사항 및 해석

**PER/PBR이 낮은 이유를 확인하세요:**

1. ✅ **진짜 저평가**: 시장이 간과한 우량 기업
2. ❌ **밸류 트랩**: 실적 악화로 인한 저평가
   - 순이익 급감 → PER 낮아짐
   - 부채 과다 → PBR 낮아짐
3. ❌ **구조적 문제**: 사양 산업, 경영 리스크

**추가 점검 사항:**
- 최근 분기 실적 추이 (개선 중인가?)
- 부채비율 (재무 건전성)
- 영업이익률 (수익성)
- 배당 여부 (주주환원)

**결과 해석:**
- PER {max_per} 이하 = 이익 대비 주가 저평가
- PBR {max_pbr} 이하 = 순자산 대비 주가 저평가
- 두 조건 동시 만족 = 밸류 투자 후보

**다음 단계:**
1. 상위 종목들의 최근 뉴스 검색
2. 재무제표 상세 분석
3. 기술적 분석 (차트 패턴)
4. 섹터 전망 확인
"""


def screen_high_momentum_stocks(
    market: str = "KOSPI",
    period_days: int = 20,
    min_return: float = 10.0,
    min_volume_increase: float = 1.5,
) -> str:
    """
    Screen for high-momentum stocks with price and volume surge.

    Args:
        market: Target market (default: "KOSPI")
        period_days: Lookback period in days (default: 20)
        min_return: Minimum return % (default: 10.0)
        min_volume_increase: Minimum volume increase ratio (default: 1.5)

    Returns:
        Formatted prompt for momentum screening
    """
    today = datetime.now().strftime("%Y%m%d")

    return f"""다음 조건으로 모멘텀 급등 종목을 스크리닝해주세요:

**스크리닝 조건**
- 시장: {market}
- 분석 기간: 최근 {period_days}일
- 최소 수익률: {min_return}% 이상
- 최소 거래량 증가: 평균 대비 {min_volume_increase}배 이상

**실행 단계**

### Step 1: 전체 종목 리스트
```
tickers = get_market_ticker_list("{today}", "{market}")
```

### Step 2: 각 종목별 OHLCV 조회 및 계산

**주의**: 전체 종목 순회는 시간이 오래 걸립니다.
- 상위 100개 시가총액 종목만 스크리닝 권장
- 또는 배치 처리 (10개씩 묶어서)

```python
results = []
for ticker in tickers[:100]:  # 상위 100개만
    df = get_stock_ohlcv(ticker, start_date, "{today}")

    # 수익률 계산
    first_close = df.iloc[0]['종가']
    last_close = df.iloc[-1]['종가']
    return_pct = ((last_close - first_close) / first_close) * 100

    # 거래량 증가율
    avg_volume = df['거래량'].mean()
    recent_volume = df.iloc[-1]['거래량']
    volume_ratio = recent_volume / avg_volume

    # 필터링
    if return_pct >= {min_return} and volume_ratio >= {min_volume_increase}:
        results.append({{
            'ticker': ticker,
            'return': return_pct,
            'volume_ratio': volume_ratio
        }})
```

### Step 3: 정렬 및 출력

수익률 기준 내림차순 정렬 후 상위 20개 표시
"""
