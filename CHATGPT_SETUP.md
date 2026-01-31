# ChatGPT Actions 설정 가이드

## 1. Custom GPT 만들기

1. ChatGPT 우측 상단 → **Explore GPTs** → **Create** 클릭
2. **Name**: "한국 주식 분석가" (또는 원하는 이름)
3. **Description**: "한국 주식 시장 데이터 분석 전문 GPT"

## 2. Instructions (시스템 프롬프트)

```
당신은 한국 주식 시장 전문 분석가입니다.

**역할:**
- KOSPI, KOSDAQ 종목 분석
- 주가 동향 및 투자자별 매매 분석
- 재무 지표 (PER, PBR, EPS) 해석

**데이터 소스:**
- pykrx-mcp API를 통한 한국거래소(KRX) 공식 데이터
- 일별 종가 기준 데이터 (실시간 아님)

**주의사항:**
- 투자 조언이 아닌 데이터 기반 정보 제공
- 과거 데이터이므로 투자 판단은 사용자 책임
- 티커 코드는 6자리 숫자 (예: 삼성전자 005930)
```

## 3. Actions 설정

### Configure 탭에서:

1. **Create new action** 클릭
2. **Import from URL** 선택
3. URL 입력:
   ```
   https://pykrx-xifs.onrender.com/openapi.json
   ```
4. **Import** 클릭

### Authentication 설정:

- **Authentication**: None (인증 불필요)

### Privacy Policy:

- **Privacy policy URL**:
  ```
  https://pykrx-xifs.onrender.com/privacy-policy
  ```

## 4. 테스트

**Configure** 탭 우측 **Preview** 패널에서 테스트:

```
삼성전자 최근 5일 주가 보여줘
```

```
네이버 PER, PBR 알려줘
```

```
코스피 시가총액 상위 10개 종목
```

## 5. 배포

1. **Configure** 탭 상단 **Publish** 클릭
2. 공개 범위 선택:
   - **Only me**: 본인만 사용
   - **Anyone with a link**: 링크 공유
   - **Public**: GPT Store 공개

## 사용 가능한 기능

### 📈 주가 조회
- 일별/월별 OHLCV 데이터
- 수정주가 지원 (주식분할, 배당 반영)

### 💰 시가총액
- 시장별 시가총액 순위
- 거래량, 거래대금

### 📊 재무 지표
- PER (주가수익비율)
- PBR (주가순자산비율)
- EPS (주당순이익)
- 배당수익률

### 💹 투자자 동향
- 기관/외국인/개인 순매수/순매도
- 일별 투자자별 거래대금

### 🎯 ETF 정보
- ETF 티커 목록
- ETF 가격 데이터

## 제한사항

- **실시간 데이터 아님**: T+1 일 종가 기준
- **휴장일 데이터 없음**: 주말/공휴일 제외
- **투자 조언 금지**: 정보 제공만 가능
- **비공식 서비스**: 상용 서비스 아님

## 문제 해결

### "API 오류" 발생 시
1. 티커 코드 확인 (6자리 숫자인지)
2. 날짜 형식 확인 (YYYYMMDD)
3. 거래일인지 확인 (주말/공휴일 제외)

### 데이터가 없다고 나올 때
- 상장 폐지 종목일 수 있음
- 날짜 범위를 좁혀서 재시도
- 최근 2-3년 데이터로 테스트

## 참고 링크

- [REST API 문서](https://pykrx-xifs.onrender.com/docs)
- [GitHub 리포지토리](https://github.com/sharebook-kr/pykrx-mcp)
- [개인정보 보호 정책](https://pykrx-xifs.onrender.com/privacy-policy)
- [pykrx 라이브러리](https://github.com/sharebook-kr/pykrx)

---

**문의사항:**
GitHub Issues: https://github.com/sharebook-kr/pykrx-mcp/issues
