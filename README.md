# pykrx-mcp

[![CI](https://github.com/sharebook-kr/pykrx-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/sharebook-kr/pykrx-mcp/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/pykrx-mcp.svg)](https://badge.fury.io/py/pykrx-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**한국 주식 시장 데이터를 AI 에이전트에게!**

`pykrx-mcp`는 한국 주식 시장 데이터 라이브러리인 [pykrx](https://github.com/sharebook-kr/pykrx)를 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 서버로 제공하는 프로젝트입니다. Claude, GPT 등 AI 에이전트가 한국 주식 데이터를 직접 조회하고 분석할 수 있도록 지원합니다.

## ✨ 주요 기능

- 📊 **실시간 한국 주식 데이터**: KOSPI, KOSDAQ 종목의 OHLCV 데이터 조회
- 🤖 **AI 에이전트 통합**: Claude Desktop 등에서 바로 사용 가능
- ⚡ **간편한 실행**: `uvx pykrx-mcp` 한 줄로 즉시 실행
- 🔄 **자동 업데이트**: pykrx 업데이트 시 자동으로 MCP 서버도 업데이트

## 🚀 빠른 시작

### Via Smithery (권장)

[Smithery](https://smithery.ai)는 MCP 서버를 위한 패키지 매니저입니다.

```bash
smithery install pykrx-mcp
```

### 설치 없이 바로 실행

```bash
uvx pykrx-mcp
```

`uv`가 설치되어 있지 않다면:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Claude Desktop 연동

Claude Desktop에서 한국 주식 데이터를 사용하려면 설정 파일을 수정하세요:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
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

설정 후 Claude Desktop을 재시작하면 한국 주식 데이터를 조회할 수 있습니다!

## 💬 스마트 프롬프트 (Prompts)

pykrx-mcp는 복잡한 워크플로우를 자동화하는 **MCP Prompts**를 제공합니다:

### 1. 종목명으로 주가 분석

종목 코드를 몰라도 회사명만으로 분석 가능:

```
prompt_analyze_stock_by_name("삼성전자", "1M", "price")
```

**자동 처리:**
- 주요 50개 종목은 ticker 자동 매핑
- 그 외 종목은 자동으로 ticker 검색 후 조회
- 주가 데이터 조회 → 분석 → 시각화까지 가이드

**Claude에서 사용 예시:**
- "삼성전자 최근 3개월 주가 분석해줘"
- "네이버 1년치 주가 추이 보여줘"

### 2. 투자자별 수급 분석

외국인/기관/개인 투자자별 매매 패턴 분석:

```
prompt_analyze_investor_flow("카카오", "3M", "foreign")
```

**자동 처리:**
- Ticker 조회 → 수급 데이터 조회
- 주가와 수급의 상관관계 분석
- 투자자별 매매 패턴 시각화

**Claude에서 사용 예시:**
- "삼성전자 외국인 수급 추이 분석해줘"
- "SK하이닉스 최근 1개월 기관 매매 보여줘"

### 3. 저평가 종목 스크리닝

PER/PBR 기준으로 저평가 종목 찾기:

```
prompt_screen_undervalued_stocks(max_per=10, max_pbr=1, market="KOSPI")
```

**자동 처리:**
- 전체 시장 스캔 → 기본 지표 조회
- PER/PBR 필터링 및 정렬
- 상위 30개 추천 종목 리스트

**Claude에서 사용 예시:**
- "PER 10 이하, PBR 1 이하 저평가 종목 찾아줘"
- "코스닥에서 저평가 종목 스크리닝해줘"

### 사용 예시

**기본 질문 (Prompts 없이):**
- "삼성전자(005930) 최근 한 달 주가 데이터를 가져와줘"
- "2024년 1월 카카오(035720) 주가 흐름을 분석해줘"
- "SK하이닉스(000660) 최근 3개월 거래량 추이를 보여줘"

**스마트 질문 (Prompts 활용):**
- "삼성전자 최근 주가 분석해줘" ← ticker 코드 불필요!
- "외국인이 많이 사고 있는 반도체 종목 찾아줘"
- "오늘 저평가 종목 추천해줘"

## 🛠️ 개발자 가이드

### 로컬 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/sharebook-kr/pykrx-mcp.git
cd pykrx-mcp

# Python 의존성 설치
uv sync --dev

# Node.js 도구 설치 (MCP Inspector)
npm install

# 서버 실행
pykrx-mcp
```

**필수 요구사항:**
- Python 3.10+
- Node.js 18+ (MCP Inspector용, [nodejs.org](https://nodejs.org)에서 설치)

**개발 명령어:**
```bash
# MCP Inspector 실행
npm run inspector

# 테스트 실행
pytest -v
# 또는
npm run test

# 코드 포맷팅
black src/
# 또는
npm run format

# 린팅
ruff check src/
# 또는
npm run lint
```

MCP Inspector는 개발 환경에 포함되어 있습니다:

```bash
npm run inspector
```

Inspector UI가 열리면 웹 브라우저에서 서버 상태, 도구 목록, 실시간 요청/응답을 확인할 수 있습니다.
```

#### 2. Claude Desktop 로그 확인

Claude Desktop과 통신하면서 발생하는 로그를 실시간으로 확인:

```bash
# macOS
tail -n 100 -f ~/Library/Logs/Claude/mcp*.log

# Windows (PowerShell)
Get-Content "$env:APPDATA\Claude\logs\mcp*.log" -Wait -Tail 100
```

#### 3. VS Code 디버거

F5 키를 눌러 VS Code 디버거로 서버를 실행하고 중단점을 설정할 수 있습니다. (`.vscode/launch.json` 설정 포함)

#### 4. 로깅 확인

서버는 모든 로그를 `stderr`로 출력합니다 (`stdout`은 MCP 프로토콜용):

```bash
# 로그를 파일로 저장하며 실행
pykrx-mcp 2> debug.log
```

### 직접 설치하여 사용

```bash
pip install pykrx-mcp
pykrx-mcp
```

## 📋 제공되는 도구 (Tools)

### get_stock_ohlcv

한국 주식의 OHLCV (시가, 고가, 저가, 종가, 거래량) 데이터를 조회합니다.

**매개변수:**
- `ticker` (str): 종목 코드 (예: "005930" - 삼성전자)
- `start_date` (str): 시작일 (YYYYMMDD 형식, 예: "20240101")
- `end_date` (str): 종료일 (YYYYMMDD 형식, 예: "20240131")
- `adjusted` (bool): 수정주가 여부 (기본값: True)

**반환값:**
날짜별 주가 데이터 (Open, High, Low, Close, Volume, 거래대금 포함)

## 🔗 관련 링크

- [pykrx 라이브러리](https://github.com/sharebook-kr/pykrx) - 한국 주식 시장 데이터의 원천
- [Model Context Protocol](https://modelcontextprotocol.io) - MCP 공식 문서
- [Smithery](https://smithery.ai) - MCP 서버 디렉토리

## 📦 자동 업데이트

`pykrx` 본체 라이브러리가 업데이트되면 `repository_dispatch` 이벤트를 통해 이 MCP 서버도 자동으로 새 버전이 배포됩니다.

**배포 프로세스:**
1. pykrx 릴리스 → `pykrx_release` 이벤트 발생
2. 의존성 자동 업데이트 (`uv lock --upgrade-package pykrx`)
3. 패치 버전 자동 증가 (예: 0.1.0 → 0.1.1)
4. Git 태그 생성 및 푸시
5. PyPI 자동 배포 (Trusted Publishing)
6. GitHub Release 생성

GitHub Actions를 통해 완전 자동화되어 있어 항상 최신 데이터 소스를 사용할 수 있습니다.

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

- 버그 리포트: [Issues](https://github.com/sharebook-kr/pykrx-mcp/issues)
- 기능 제안: [Discussions](https://github.com/sharebook-kr/pykrx-mcp/discussions)

---

**Made with ❤️ by sharebook-kr**
