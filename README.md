# pykrx-mcp

**한국 주식 시장 데이터를 AI 에이전트에게!**

`pykrx-mcp`는 한국 주식 시장 데이터 라이브러리인 [pykrx](https://github.com/sharebook-kr/pykrx)를 [Model Context Protocol (MCP)](https://modelcontextprotocol.io) 서버로 제공하는 프로젝트입니다. Claude, GPT 등 AI 에이전트가 한국 주식 데이터를 직접 조회하고 분석할 수 있도록 지원합니다.

## ✨ 주요 기능

- 📊 **실시간 한국 주식 데이터**: KOSPI, KOSDAQ 종목의 OHLCV 데이터 조회
- 🤖 **AI 에이전트 통합**: Claude Desktop 등에서 바로 사용 가능
- ⚡ **간편한 실행**: `uvx pykrx-mcp` 한 줄로 즉시 실행
- 🔄 **자동 업데이트**: pykrx 업데이트 시 자동으로 MCP 서버도 업데이트

## 🚀 빠른 시작

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

### 사용 예시

Claude에게 다음과 같이 요청해보세요:

- "삼성전자(005930) 최근 한 달 주가 데이터를 가져와줘"
- "2024년 1월 카카오(035720) 주가 흐름을 분석해줘"
- "SK하이닉스(000660) 최근 3개월 거래량 추이를 보여줘"

## 🛠️ 개발자 가이드

### 로컬 개발 환경 설정

```bash
# 저장소 클론
git clone https://github.com/sharebook-kr/pykrx-mcp.git
cd pykrx-mcp

# 의존성 설치 (editable mode)
uv pip install -e .

# 서버 실행 (stdio 모드로 실행되어 MCP 통신 대기)
pykrx-mcp
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
