---
name: fetch-brunch
description: brunch.co.kr 글의 본문을 markdown으로 가져오거나, 특정 작가(@username)의 글 목록을 탐색할 때 사용합니다. AI_TOP_100 챌린지 문제는 카카오(@andkakao)의 브런치에서 연재되므로, 신규 챌린지 본문을 수집해야 할 때 반드시 이 skill을 사용하세요. brunch URL을 다루거나 "brunch에서 가져와", "@andkakao 글 찾아" 같은 요청에 트리거됩니다.
---

# fetch-brunch

brunch.co.kr 글 본문을 markdown으로 변환해 가져오는 skill입니다.
기존 `utils/crawl_questions.py`의 단일 URL 수집 로직을 재사용 가능한 형태로 분리한 것입니다.

## 언제 사용하나요

- 특정 brunch 글 URL의 본문을 추출해야 할 때
- `@andkakao` 같은 작가 프로필에서 최신 글 목록을 살펴봐야 할 때
- AI_TOP_100 신규 회차 문제 글을 찾아야 할 때

## 제공하는 스크립트

```
fetch-brunch/
├── SKILL.md
└── scripts/
    ├── fetch_one.py       # 단일 URL → markdown
    └── list_author.py     # 작가 페이지 → 글 목록 JSON
```

## 사용 방법

### 1. 단일 글 본문 추출

```bash
uv run --with requests --with beautifulsoup4 --with markdownify \
  python .claude/skills/fetch-brunch/scripts/fetch_one.py <URL>
```

표준출력에 `# {title}\n\nSource: {url}\n\n{markdown body}` 형식의 markdown을 출력합니다.
파일로 저장하고 싶다면 `>` 리다이렉트.

예시:
```bash
python .claude/skills/fetch-brunch/scripts/fetch_one.py \
  https://brunch.co.kr/@andkakao/317 > /tmp/q1.md
```

### 2. 작가 글 목록 탐색

```bash
python .claude/skills/fetch-brunch/scripts/list_author.py @andkakao
```

JSON 배열을 출력합니다 (각 항목: `{"id": 317, "title": "...", "url": "..."}`).

키워드 필터:
```bash
python .claude/skills/fetch-brunch/scripts/list_author.py @andkakao --filter "AI_TOP_100"
```

## 동작 원리

brunch의 글 페이지는 SSR이라 단순 HTTP GET으로 HTML을 받아옵니다.
본문은 `<div class="wrap_body">` 안에 들어있고, 제목은 `<h1 class="cover_title">`에 있습니다.
`markdownify`로 HTML → markdown 변환.

작가 목록 페이지는 `https://brunch.co.kr/@username` (또는 `/@username/N`)에서 시작하며,
페이지네이션은 `?` 쿼리로 처리됩니다. 셀렉터 디테일은 `references/selectors.md` 참고.

## 실패 시

- 403/429: brunch에서 봇 차단 — User-Agent 헤더 변경
- 본문이 비어있음: `wrap_body` 셀렉터가 깨졌는지 확인
- 작가 목록이 0건: `https://brunch.co.kr/@andkakao` 직접 방문해 마크업 변경 확인
