---
name: fetch-aitop
description: challenge.aitop100.org에서 AI_TOP_100 챌린지 문제 메타데이터와 상세 정보를 가져올 때 사용합니다. 사이트는 SPA라 일반 fetch로는 본문을 못 받지만, 백엔드에 공개 JSON API(/api/problems)가 있어 21개 챌린지 전체 메타데이터를 인증 없이 받을 수 있습니다. 상세 페이지는 카카오 로그인 쿠키가 필요하며, 이 skill은 쿠키 파일을 받아 인증된 요청을 보내는 헬퍼를 제공합니다. "aitop100", "AI_TOP_100 문제 목록", "신규 챌린지 가져와" 같은 요청에 트리거됩니다.
---

# fetch-aitop

challenge.aitop100.org의 챌린지 메타데이터/상세를 가져오는 skill입니다.

## 사이트 구조 요약

- 프론트엔드: Vite + React SPA. HTML에는 `<div id="root">`만 있어서 `requests`로는 본문을 못 받습니다.
- 백엔드 API: `https://challenge.aitop100.org/api/...` (Spring 기반으로 추정)
  - `GET /api/problems` — **공개**. 21개 챌린지 전체 메타데이터 + 시즌 정보 반환. (검증됨)
  - `GET /api/problem/{code}` — 404 (엔드포인트 다름)
  - `GET /api/problems/{code}` — 403 (인증 필요)
  - 상세 엔드포인트는 미확정 — `fetch_detail.py`가 여러 후보를 시도합니다.

## 제공하는 스크립트

```
fetch-aitop/
├── SKILL.md
├── scripts/
│   ├── list_problems.py  # /api/problems → JSON / 표
│   └── fetch_detail.py   # 상세 페이지 (인증 필요)
└── references/
    └── api.md            # 엔드포인트와 응답 스키마 메모
```

## 사용 방법

### 1. 전체 챌린지 목록

```bash
uv run --with requests -- python .claude/skills/fetch-aitop/scripts/list_problems.py
```

JSON 그대로 출력. 시즌 필터링은 `--season 5` 같이 지정.
표 형식 보고 싶으면 `--format table`.

### 2. 상세 페이지 (인증 필요)

먼저 브라우저에서 challenge.aitop100.org에 로그인한 뒤,
**EditThisCookie** 같은 확장으로 challenge.aitop100.org 도메인 쿠키를 export합니다.
(Netscape 또는 JSON 포맷 모두 지원)

저장 위치 권장: `~/.aitop_cookies.json`

```bash
python .claude/skills/fetch-aitop/scripts/fetch_detail.py csatmyth \
  --cookies ~/.aitop_cookies.json
```

상세를 얻지 못하면 fallback으로 `/api/problems` summary만 반환합니다.

## 쿠키 export 가이드

크롬/엣지 기준:
1. challenge.aitop100.org 로그인
2. EditThisCookie 확장 설치 → 사이트 방문 중 우상단 아이콘 클릭
3. "Export" → JSON 형식 선택 → 클립보드에 복사
4. `~/.aitop_cookies.json`에 붙여넣기 (한 JSON 배열)

쿠키 만료 시 다시 export. (보통 며칠 ~ 몇 주 유지됨)

## 실패 시

- 401/403: 쿠키 만료 또는 도메인 불일치 — 다시 export
- 404: 엔드포인트가 바뀐 것 — `references/api.md` 업데이트 + 후보 path 추가
- SPA가 데이터를 별도 호출 없이 임베드한다면 (가능성 낮음): Playwright 도입 검토
