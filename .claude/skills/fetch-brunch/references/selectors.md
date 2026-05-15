# brunch HTML 셀렉터 메모

마크업이 바뀌면 여기 적힌 셀렉터부터 점검하세요. (마지막 확인: 2026-05)

## 글 페이지 (`/@user/N`)

| 항목 | 셀렉터 | 비고 |
|------|--------|------|
| 제목 | `h1.cover_title` | fallback: `<title>` |
| 본문 | `div.wrap_body` | 광고/네비 제외하기 위해 본문 컨테이너 사용 |
| og:title | `meta[property="og:title"]` | h1 누락 시 차선책 |
| 작성일 | `span.date` | 현재는 미수집 |

## 작가 페이지 (`/@user`)

작가 페이지 자체는 React로 lazy-render되어 글 목록을 HTML에서 직접 얻기 어렵습니다.
`list_author.py`는 id를 순차 probing해서 200 응답 + h1.cover_title을 가진 글만 수집합니다.

브런치 글 id는 작성 순서대로 증가하므로, 신규 글을 찾으려면 알려진 마지막 id 이후를
probing하면 됩니다. 예: `--start 328 --end 400`.

## 차단 회피

- `User-Agent` 헤더 필수 (없으면 종종 403)
- 동시 요청 8개 이하로 유지 (`list_author.py`의 `--workers`)
- 429 발생 시 sleep 후 재시도
