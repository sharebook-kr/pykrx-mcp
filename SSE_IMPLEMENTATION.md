# SSE 서버 구현 완료

## 변경 사항 요약

pykrx-mcp가 이제 SSE (Server-Sent Events) 서버로 작동하며 Render에 배포할 수 있습니다.

### 새로 추가된 파일

1. **src/pykrx_mcp/asgi.py**
   - ASGI 진입점
   - uvicorn으로 직접 실행 가능
   - FastMCP의 `sse_app` 사용

2. **src/pykrx_mcp/main.py**
   - Render 배포용 래퍼
   - 환경 변수 설정
   - server.main() 위임

3. **render.yaml**
   - Render Blueprint 설정
   - 원클릭 배포 지원
   - 무료 플랜 구성

4. **RENDER_DEPLOYMENT.md**
   - 상세한 배포 가이드
   - 트러블슈팅
   - 로컬 테스트 방법

### 수정된 파일

1. **src/pykrx_mcp/server.py**
   - FastMCP API 수정 (`host`/`port` → 환경 변수)
   - `--mount-path` 인수 추가
   - uvicorn 환경 변수 안내 추가

2. **pyproject.toml**
   - FastAPI 의존성 추가: `fastapi>=0.115.0`
   - Uvicorn 의존성 추가: `uvicorn[standard]>=0.32.0`
   - 새 진입점 추가: `pykrx-mcp-sse`

3. **README.md**
   - Render 배포 섹션 간소화
   - RENDER_DEPLOYMENT.md 링크 추가
   - 로컬 SSE 테스트 명령어 추가

## 사용 방법

### 로컬 개발 (stdio 모드)
```bash
pykrx-mcp
```

### 로컬 SSE 서버
```bash
# 방법 1: 직접 uvicorn 사용 (권장)
uv run uvicorn pykrx_mcp.asgi:app --host 0.0.0.0 --port 8000

# 방법 2: 래퍼 스크립트 사용
pykrx-mcp-sse

# 방법 3: main 모듈 직접 실행
python -m pykrx_mcp.main
```

### Render 배포
1. GitHub에 푸시
2. Render Dashboard에서 Blueprint로 배포
3. `render.yaml` 자동 감지

## 기술 세부사항

### FastMCP SSE 지원

FastMCP는 `run(transport="sse")` 호출 시 내부적으로:
- SSE용 ASGI 앱 생성 (`mcp.sse_app` 속성)
- uvicorn을 통해 서버 실행
- 환경 변수로 구성: `HOST`, `PORT`

### ASGI 진입점 (asgi.py)

```python
from pykrx_mcp.server import mcp
app = mcp.sse_app  # ASGI callable
```

이 방식으로:
- 표준 ASGI 서버와 호환 (uvicorn, gunicorn, hypercorn 등)
- Render의 자동 포트 할당 ($PORT) 지원
- 컨테이너 배포 가능 (Docker, Kubernetes 등)

## 테스트 완료

✅ 로컬 SSE 서버 실행 (포트 8001)
✅ curl로 /sse 엔드포인트 접속 확인
✅ ASGI 앱 로드 테스트
✅ render.yaml 구문 검증

## 다음 단계

1. GitHub에 푸시
2. Render에 배포 테스트
3. 실제 Claude Desktop에서 원격 연결 테스트
4. 프로덕션 환경 고려사항 문서화
