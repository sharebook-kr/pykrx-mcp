# Koyeb 배포 가이드

## Koyeb란?

Koyeb는 Docker 컨테이너를 쉽게 배포할 수 있는 서버리스 플랫폼입니다.
- 무료 플랜 제공 (월 $5.5 크레딧)
- 자동 HTTPS
- 전 세계 엣지 배포
- GitHub 연동 자동 배포

## 사전 준비

1. [Koyeb 계정 생성](https://app.koyeb.com/auth/signup)
2. GitHub 리포지토리 연동

## 배포 방법

### 1. Koyeb 대시보드 접속

https://app.koyeb.com 로그인

### 2. 새 서비스 생성

1. **Create Service** 클릭
2. **GitHub** 선택
3. 리포지토리 선택: `sharebook-kr/pykrx-mcp`
4. Branch: `main`

### 3. 빌드 설정

**Builder:** Docker

**Dockerfile path:** `Dockerfile`

**Build context:** `/` (루트)

### 4. 환경 변수 설정 (선택사항)

필요한 경우 환경 변수 추가:
```
PORT=8000
PYTHONUNBUFFERED=1
```

### 5. 인스턴스 설정

**Instance type:** 
- Free tier: `nano` (512MB RAM, 0.1 vCPU)
- Paid: `small` 이상 권장

**Regions:**
- `fra` (Frankfurt) - 유럽 사용자
- `was` (Washington) - 미국 사용자
- `sin` (Singapore) - 아시아 사용자

**Scaling:**
- Min instances: 1
- Max instances: 1 (무료 플랜)

### 6. 포트 설정

**Port:** 8000

**Protocol:** HTTP

**Path:** `/` (health check를 위해 `/health` 권장)

### 7. 헬스 체크 설정

**Health check path:** `/health`

**Health check interval:** 10s

**Health check timeout:** 5s

### 8. 배포

**Service name:** `pykrx-mcp` (또는 원하는 이름)

**Deploy** 클릭!

## 배포 후 확인

배포가 완료되면 다음 URL로 접속 가능:
```
https://pykrx-mcp-<your-app-id>.koyeb.app
```

### API 테스트

```bash
# Health check
curl https://pykrx-mcp-<your-app-id>.koyeb.app/health

# OpenAPI docs
curl https://pykrx-mcp-<your-app-id>.koyeb.app/docs

# Privacy policy
curl https://pykrx-mcp-<your-app-id>.koyeb.app/privacy-policy

# Stock data test
curl -X POST https://pykrx-mcp-<your-app-id>.koyeb.app/tools/get_stock_ohlcv \
  -H "Content-Type: application/json" \
  -d '{"ticker": "005930", "start_date": "20210115", "end_date": "20210122", "adjusted": true}'
```

## 자동 배포 설정

GitHub의 `main` 브랜치에 push하면 자동으로 재배포됩니다.

### 배포 트리거:
- Git push to `main` branch
- Manual redeploy (Koyeb 대시보드에서)

## ChatGPT Actions 업데이트

배포 완료 후 ChatGPT Custom GPT Actions 설정 업데이트:

1. **OpenAPI URL 변경:**
   ```
   https://pykrx-mcp-<your-app-id>.koyeb.app/openapi.json
   ```

2. **Privacy Policy URL 변경:**
   ```
   https://pykrx-mcp-<your-app-id>.koyeb.app/privacy-policy
   ```

## 트러블슈팅

### 빌드 실패

**문제:** Docker 빌드 중 오류 발생

**해결:**
- `uv.lock` 파일이 최신인지 확인
- `pyproject.toml`의 의존성 확인
- Dockerfile의 Python 버전 확인 (3.11)

### 서비스 시작 실패

**문제:** 컨테이너가 시작되지 않음

**해결:**
- Koyeb 로그 확인 (Dashboard → Service → Logs)
- 포트 설정 확인 (8000)
- Health check path 확인 (`/health`)

### 메모리 부족

**문제:** OOM (Out of Memory) 오류

**해결:**
- 인스턴스 타입을 `small` 이상으로 업그레이드
- 무료 플랜에서는 512MB 제한

### API 응답 느림

**문제:** 첫 요청이 느림 (cold start)

**해결:**
- Koyeb의 서버리스 특성상 첫 요청은 느릴 수 있음
- Paid 플랜에서는 "Always On" 옵션 사용
- 또는 정기적으로 health check 요청 (cron job)

## 로컬 Docker 테스트

배포 전 로컬에서 테스트:

```bash
# Docker 이미지 빌드
docker build -t pykrx-mcp .

# 컨테이너 실행
docker run -p 8000:8000 pykrx-mcp

# 테스트
curl http://localhost:8000/health
```

## 비용

**무료 플랜:**
- $5.5/월 크레딧
- nano 인스턴스 (~$5/월)
- 충분히 개발/테스트 가능

**유료 플랜:**
- small: $11/월 (1GB RAM, 0.5 vCPU)
- medium: $22/월 (2GB RAM, 1 vCPU)
- 프로덕션 환경 권장

## 참고 링크

- [Koyeb Documentation](https://www.koyeb.com/docs)
- [Koyeb Docker Deployment](https://www.koyeb.com/docs/deploy/docker)
- [Koyeb GitHub Integration](https://www.koyeb.com/docs/build-and-deploy/github)

---

**문의:** [GitHub Issues](https://github.com/sharebook-kr/pykrx-mcp/issues)
