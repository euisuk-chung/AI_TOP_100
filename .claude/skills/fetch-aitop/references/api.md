# aitop100.org API 메모

마지막 확인: 2026-05.

## 기본

- 베이스: `https://challenge.aitop100.org`
- 백엔드는 Spring 기반으로 추정 (에러 응답에 `timestamp`/`status`/`error`/`message` 필드)

## 공개 엔드포인트

### `GET /api/problems`

전체 챌린지 목록 + 시즌 정보. 인증 불필요.

응답 스키마:
```jsonc
{
  "problems": [
    {
      "code": "csatmyth",
      "orderIndex": 0,
      "title": "수능 경향 분석",
      "shortTitle": "수능 분석",
      "summary": "...",
      "thumbnail": "https://t1.kakaocdn.net/aitop_public/thumbnail/csatmyth.png",
      "categories": ["분석"],
      "seasonId": 5,
      "solved": null,
      "score": null,
      "gradingStatus": null
    }
    // ... 총 21개
  ],
  "seasons": [
    {
      "id": 5,
      "title": "AI_TOP_100 (CAMPUS) 본선",
      "description": "...",
      "isActive": false,
      "effectiveFrom": "2026-04-15T14:00:00",
      "effectiveUntil": "2026-04-28T23:59:00"
    }
    // ... id 1~5
  ]
}
```

## 보호된 엔드포인트 (인증 필요)

확정된 path는 없지만 다음 후보를 시도:
- `GET /api/problems/{code}` → **403 ACCESS_DENIED** (쿠키 필요)
- `GET /api/problem/{code}` → **404 NOT_FOUND** (path 오류)
- `GET /api/problems/{code}/detail` → 미확인
- `GET /api/problems/{code}/description` → 미확인

상세 응답 스키마는 인증 후 캡처해서 여기에 추가하세요.

## 인증

카카오 OAuth 기반으로 추정. 쿠키는 보통 `JSESSIONID`, `aitop_session` 같은 이름.
`fetch_detail.py`에 쿠키 파일 경로를 넘기면 자동 로드.

## 시즌 매핑

| seasonId | title | 시기 |
|----------|-------|------|
| 1 | AI_TOP_100 #1 | 2025-12-02 ~ 12-17 (예선 5 + 본선 1) |
| 2 | AI_TOP_100 #2 | 2025-12-18 ~ 12-30 (본선 2) |
| 3 | AI_TOP_100 #3 | 2025-12-31 ~ 2026-01-13 (본선 3) |
| 4 | AI_TOP_100 (CAMPUS) 예선 | 2026-04-08 ~ 04-14 (예선 5) |
| 5 | AI_TOP_100 (CAMPUS) 본선 | 2026-04-15 ~ 04-28 (본선 5) |
