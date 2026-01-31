# pykrx-mcp

[![PyPI version](https://badge.fury.io/py/pykrx-mcp.svg)](https://badge.fury.io/py/pykrx-mcp)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Open in Dev Containers](https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/sharebook-kr/pykrx-mcp)
<a href="https://open.kakao.com/o/gQd1AM3"><img src="https://img.shields.io/badge/kakao-pykrx-yellow.svg"></a>

한국 주식 시장 데이터를 AI 에이전트에게 제공하는 MCP 서버입니다.

KOSPI, KOSDAQ 종목의 주가, 시가총액, 재무제표 등을 Claude Desktop에서 바로 조회할 수 있습니다.

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

### 사용 예시
```
삼성전자 최근 한달 주가 보여줘
코스피 시가총액 상위 10개 종목은?
```

---

## 📊 제공되는 데이터

- **주가 데이터**: 일별 시가/고가/저가/종가/거래량
- **종목 정보**: 종목 코드, 종목명, 시장 구분
- **시가총액**: 시장별 시가총액 순위
- **재무 데이터**: PER, PBR, EPS, 배당수익률
- **투자자별 수급**: 기관/외국인/개인 매매 동향
- **ETF 데이터**: ETF 가격 및 종목 정보

---

## 🛠️ 개발자 가이드

프로젝트에 기여하거나 직접 배포하려면 다음 문서를 참고하세요:

- [개발 가이드](./DEVELOPMENT.md) - 로컬 개발 환경 설정
- [Koyeb 배포 가이드](./KOYEB_DEPLOY.md) - Docker 기반 웹서버 배포

---

## 🔗 관련 링크

- [pykrx 라이브러리](https://github.com/sharebook-kr/pykrx) - 데이터 소스
- [MCP Protocol](https://modelcontextprotocol.io) - 프로토콜 사양
- [커뮤니티 (카카오톡)](https://open.kakao.com/o/gQd1AM3) - 질문 및 피드백

---

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

- 버그 리포트: [Issues](https://github.com/sharebook-kr/pykrx-mcp/issues)
- 기능 제안: [Discussions](https://github.com/sharebook-kr/pykrx-mcp/discussions)

---

**Made with ❤️ by sharebook-kr**

## 📄 라이선스

MIT License - 자유롭게 사용하세요!

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

- 버그 리포트: [Issues](https://github.com/sharebook-kr/pykrx-mcp/issues)
- 기능 제안: [Discussions](https://github.com/sharebook-kr/pykrx-mcp/discussions)

---

**Made with ❤️ by sharebook-kr**
