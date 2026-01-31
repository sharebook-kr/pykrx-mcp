# pykrx-mcp

[![PyPI version](https://badge.fury.io/py/pykrx-mcp.svg)](https://badge.fury.io/py/pykrx-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/sharebook-kr/pykrx-mcp)

한국 주식 시장 데이터를 AI 에이전트에게 제공하는 MCP 서버입니다.

KOSPI, KOSDAQ 종목의 주가, 시가총액, 재무제표 등을 ChatGPT, Claude에서 바로 조회할 수 있습니다.

---

## ☕ 후원하기

프로젝트가 도움이 되었다면 개발자를 응원해주세요!

[![Sponsor](https://img.shields.io/badge/Sponsor-GitHub-pink?style=for-the-badge&logo=github)](https://github.com/sponsors/sharebook-kr)

---

## 🚀 ChatGPT에서 사용하기

**pykrx GPT 다운로드:** [https://chatgpt.com/g/g-697e184a14e48191b765bfd43037bd35-pykrx](https://chatgpt.com/g/g-697e184a14e48191b765bfd43037bd35-pykrx)

GPT Store에서 pykrx GPT를 다운로드하면 바로 사용할 수 있습니다.

---

## 🤖 Claude Desktop에서 사용하기

### MCP Registry 설치 (권장)

```bash
npx @modelcontextprotocol/inspector install pykrx-mcp
```

### 또는 수동 설정

`~/Library/Application Support/Claude/claude_desktop_config.json`:
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

Claude Desktop 재시작 후 한국 주식 데이터를 바로 사용할 수 있습니다.

---

## 📊 제공되는 데이터

- **주가 데이터**: 일별 시가/고가/저가/종가/거래량
- **종목 정보**: 종목 코드, 종목명, 시장 구분
- **시가총액**: 시장별 시가총액 순위
- **재무 데이터**: PER, PBR, EPS, 배당수익률
- **투자자별 수급**: 기관/외국인/개인 매매 동향
- **ETF 데이터**: ETF 가격 및 종목 정보

---

## � 지원하는 질문

**📈 주가 조회**
- "삼성전자 최근 한달 주가 보여줘"
- "SK하이닉스 2024년 1월 OHLCV 데이터"
- "카카오 지난주 주가 움직임 분석해줘"

**💰 시가총액 & 거래량**
- "삼성전자 시가총액이 얼마야?"
- "삼성전자 최근 한달 거래량 보여줘"
- "카카오 거래대금 추이 알려줘"

**📊 재무 지표**
- "삼성전자 PER, PBR 알려줘"
- "삼성전자 배당수익률 얼마야?"
- "네이버 최근 EPS는 얼마야?"

**👥 투자자별 수급**
- "삼성전자 외국인 매수세 어때?"
- "카카오 최근 기관 수급 분석해줘"
- "LG전자 개인 투자자 거래 추이 알려줘"

**🔍 종목 검색**
- "코스피 종목 리스트 알려줘"
- "005930 종목명이 뭐야?"
- "오늘 거래된 ETF 리스트 보여줘"

---

## 📄 라이선스

MIT License - 자유롭게 사용하세요!
