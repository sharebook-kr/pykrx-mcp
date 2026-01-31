# pykrx-mcp

[![PyPI version](https://badge.fury.io/py/pykrx-mcp.svg)](https://badge.fury.io/py/pykrx-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

한국 주식 시장 데이터를 AI 에이전트에게 제공하는 MCP 서버입니다.

KOSPI, KOSDAQ 종목의 실시간 주가, 시가총액, 재무제표 등을 ChatGPT, Claude에서 바로 조회할 수 있습니다.

---

## 🚀 ChatGPT에서 사용하기

**상세 가이드:** [CHATGPT_SETUP.md](./CHATGPT_SETUP.md)

### 1. Custom GPT 생성
ChatGPT 우측 상단 → **Explore GPTs** → **Create**

### 2. Actions 설정
**Configure** 탭 → **Create new action** → **Import from URL**

공개 REST API 엔드포인트 (곧 제공 예정)

### 3. 바로 사용
"삼성전자 최근 한달 주가 보여줘"

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

---

## � 배포

**Koyeb 배포 가이드:** [KOYEB_DEPLOY.md](./KOYEB_DEPLOY.md)

Docker 기반 배포를 지원합니다:
```bash
docker build -t pykrx-mcp .
docker run -p 8000:8000 pykrx-mcp
```

---

## 🔗 관련 링크

- [ChatGPT 설정 가이드](./CHATGPT_SETUP.md) - Custom GPT Actions 설정
- [Koyeb 배포 가이드](./KOYEB_DEPLOY.md) - Docker 배포
- [pykrx 라이브러리](https://github.com/sharebook-kr/pykrx) - 데이터 소스
- [MCP Protocol](https://modelcontextprotocol.io) - 프로토콜 사양

---

## 📄 라이선스

MIT License

**Made with ❤️ by sharebook-kr**

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
