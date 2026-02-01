# pykrx-mcp

[![PyPI version](https://badge.fury.io/py/pykrx-mcp.svg)](https://badge.fury.io/py/pykrx-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/sharebook-kr/pykrx-mcp)

한국 주식 시장 데이터를 AI 에이전트에게 제공하는 MCP (Model Context Protocol) 서버입니다.

[pykrx](https://github.com/sharebook-kr/pykrx) 라이브러리를 기반으로 KOSPI, KOSDAQ, KONEX 시장의 주가, 재무제표, 투자자별 수급, 공매도 등 다양한 데이터를 ChatGPT와 Claude에서 자연어로 조회할 수 있습니다.

---

## ☕ 후원하기

프로젝트가 도움이 되었다면 개발자를 응원해주세요!

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/sharebook-kr)

---

## 1. 시작하기

### 1.1 ChatGPT에서 사용하기

#### GPT Store 다운로드 (권장)

**pykrx GPT**: [https://chatgpt.com/g/g-697e184a14e48191b765bfd43037bd35-pykrx](https://chatgpt.com/g/g-697e184a14e48191b765bfd43037bd35-pykrx)

GPT Store에서 pykrx GPT를 추가하면 바로 사용할 수 있습니다.

> **참고**: [Koyeb](https://app.koyeb.com/) 서비스를 통해 무료로 호스팅되고 있습니다.

### 1.2 Claude Desktop에서 사용하기

#### 자동 설치 (권장)

MCP Registry를 통한 원클릭 설치:

```bash
npx @modelcontextprotocol/inspector install pykrx-mcp
```

#### 수동 설치

Claude Desktop 설정 파일을 직접 수정:

**macOS/Linux**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "pykrx": {
      "command": "uvx",
      "args": ["pykrx-mcp"]
    }
  }
}
```

설정 후 Claude Desktop을 재시작하면 바로 사용할 수 있습니다.

---

## 2. 지원하는 데이터 및 API

> 모든 API는 [pykrx 라이브러리](https://github.com/sharebook-kr/pykrx)를 기반으로 구현되었습니다.

### 2.1 주식 데이터 (Stock Data)

#### 2.1.1 종목 정보
- `get_market_ticker_list`: 시장별 종목 코드 조회
- `get_market_ticker_name`: 종목 코드로 종목명 조회

#### 2.1.2 가격 데이터
- `get_stock_ohlcv`: 개별 종목 OHLCV (시가/고가/저가/종가/거래량)
- `get_market_ohlcv_by_date`: 특정 일자 전종목 시세
- `get_market_price_change`: 기간별 전종목 가격 변동

#### 2.1.3 시가총액
- `get_market_cap_by_date`: 개별 종목 시가총액 조회

#### 2.1.4 재무 지표
- `get_market_fundamental_by_date`: PER, PBR, EPS, DIV, BPS, DPS

#### 2.1.5 투자자별 거래
- `get_market_trading_value_by_date`: 종목별 투자자 수급 (거래대금)
- `get_market_trading_volume_by_investor`: 투자자별 거래량
- `get_market_trading_value_by_investor`: 투자자별 거래대금
- `get_market_net_purchases_of_equities`: 투자자별 순매수 상위 종목

### 2.2 지수 데이터 (Index Data)

#### 2.2.1 지수 정보
- `get_index_ticker_list`: 지수 티커 목록
- `get_index_ticker_name`: 지수 이름 조회
- `get_index_portfolio_deposit_file`: 지수 구성 종목

#### 2.2.2 지수 가격
- `get_index_ohlcv`: 지수 OHLCV 데이터

#### 2.2.3 지수 지표
- `get_index_fundamental`: 지수 PER/PBR/배당수익률

### 2.3 공매도 데이터 (Short Selling)

- `get_shorting_status_by_date`: 종목별 공매도 현황
- `get_shorting_volume_by_ticker`: 전종목 공매도 거래량
- `get_shorting_balance_top50`: 공매도 잔고 상위 50
- `get_shorting_volume_top50`: 공매도 거래 비중 상위 50

### 2.4 외국인 투자 (Foreign Investment)

- `get_exhaustion_rates_of_foreign_investment`: 외국인 보유량 및 한도소진률

### 2.5 ETF 데이터

- `get_etf_ticker_list`: ETF 종목 리스트
- `get_etf_ohlcv_by_date`: ETF OHLCV 데이터

**총 23개의 데이터 조회 도구 지원**

---

## 3. 사용 예시

### 3.1 주가 조회

**개별 종목 주가**
```
"삼성전자 최근 한달 주가 보여줘"
"SK하이닉스 2024년 1월 OHLCV 데이터"
"카카오 지난주 주가 움직임 분석해줘"
```

**시장 전체 시세**
```
"코스피 전종목 오늘 시세 보여줘"
"코스닥 상위 10개 종목 가격 변동률"
```

### 3.2 시가총액 & 거래량

```
"삼성전자 시가총액이 얼마야?"
"삼성전자 최근 한달 거래량 추이"
"네이버 거래대금 분석해줘"
```

### 3.3 재무 지표

```
"삼성전자 PER, PBR 알려줘"
"삼성전자 배당수익률 얼마야?"
"네이버 최근 EPS는?"
```

### 3.4 투자자별 수급 분석

```
"삼성전자 외국인 매수세 어때?"
"카카오 최근 기관 수급 분석"
"코스피 개인 투자자가 많이 산 종목"
"외국인이 순매수한 상위 10개 종목"
```

### 3.5 공매도 분석

```
"삼성전자 공매도 비중 얼마야?"
"코스피 공매도 상위 종목 알려줘"
"공매도 잔고가 가장 높은 종목은?"
```

### 3.6 지수 조회

```
"코스피 지수 최근 한달 추이"
"코스닥 150 지수 PER은?"
"반도체 섹터 지수 구성 종목 알려줘"
```

### 3.7 외국인 투자

```
"삼성전자 외국인 보유 비중은?"
"외국인 한도소진률 높은 종목"
```

### 3.8 종목 검색

```
"코스피 종목 리스트"
"005930 종목명이 뭐야?"
"오늘 거래된 ETF 리스트"
```

---

## 4. 주요 특징

### 4.1 자연어 대화형 인터페이스
복잡한 API 문법 없이 일상 언어로 데이터를 조회할 수 있습니다.

### 4.2 실시간 한국 주식 시장 데이터
KRX(한국거래소)의 최신 데이터를 제공합니다.

### 4.3 다양한 분석 기능
- 가격 추이 분석
- 투자자별 수급 분석
- 재무 지표 비교
- 공매도 현황 분석

### 4.4 AI 에이전트 최적화
ChatGPT와 Claude에서 바로 사용할 수 있도록 MCP 프로토콜을 지원합니다.

---

## 5. 기술 스택

- **Python 3.10+**
- **[pykrx](https://github.com/sharebook-kr/pykrx)**: 한국 주식 시장 데이터 수집
- **[FastMCP](https://github.com/jlowin/fastmcp)**: MCP 서버 프레임워크
- **MCP (Model Context Protocol)**: AI 에이전트와의 통신 프로토콜

---

## 6. 개발자 정보

### 6.1 로컬 개발 환경 설정

자세한 내용은 [DEVELOPMENT.md](DEVELOPMENT.md)를 참고하세요.

```bash
# 저장소 클론
git clone https://github.com/sharebook-kr/pykrx-mcp.git
cd pykrx-mcp

# 의존성 설치
uv pip install -e ".[dev]"

# 테스트 실행
uv run pytest

# 서버 실행
uv run pykrx-mcp
```

### 6.2 기여하기

이슈 및 풀 리퀘스트를 환영합니다!

---

## 7. 라이선스

MIT License - 자유롭게 사용하세요!

---

## 8. 관련 프로젝트

- **[pykrx](https://github.com/sharebook-kr/pykrx)**: 한국 주식 시장 데이터 수집 라이브러리 (본 프로젝트의 기반)
- **[MCP](https://modelcontextprotocol.io/)**: Model Context Protocol 공식 문서
