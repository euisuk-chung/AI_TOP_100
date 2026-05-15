# AI_TOP_100 문제 풀이 플랫폼

이 프로젝트는 카카오임팩트와 브라이언임팩트가 주최한 'AI_TOP_100' 대회의 예선 및 본선 문제들을 수집하고, 이를 로컬 환경에서 직접 풀어볼 수 있도록 돕는 학습용 플랫폼입니다.

> **문제 출처**: [카카오 브런치 - AI TOP 100](https://brunch.co.kr/@andkakao/) 및 [challenge.aitop100.org](https://challenge.aitop100.org/)

**현재 수록된 챌린지**: 22개 (시즌 1 본선 2 / 예선 5, 시즌 2 본선 2, 시즌 3 본선 3, 시즌 4 CAMPUS 예선 5, 시즌 5 CAMPUS 본선 5)

<p align="center">
  <img src="assets/sample_detail.png" width="100%" alt="Problem Detail">
</p>

## 프로젝트 취지

이 프로젝트는 다음과 같은 목적을 가지고 만들어졌습니다.

1.  **쉬운 문제 풀이를 위한 웹 제공**: 복잡한 설정 없이 웹 브라우저에서 바로 문제를 확인하고 풀 수 있는 환경을 제공합니다.
2.  **개인 SOLVE 아카이빙 및 공유**: 사용자가 작성한 답안을 체계적으로 저장하고 관리할 수 있도록 지원합니다.

## 프로젝트 구성

이 프로젝트는 크게 두 가지 부분으로 나뉩니다.

1.  **문제 수집 (Crawling)**: 브런치(brunch.co.kr)에 공개된 문제들을 자동으로 수집하여 Markdown 형식으로 저장합니다.
2.  **문제 풀이 플랫폼 (Platform)**: 수집된 문제들을 조회하고, 코드를 작성하여 솔루션을 저장할 수 있는 웹 애플리케이션입니다.

## 시작하기

### 필수 요건

-   Python 3.8 이상
-   Node.js 18 이상
-   `uv` (Python 패키지 매니저)

### 설치 및 실행

1.  **저장소 클론 및 이동**
    ```bash
    git clone <repository-url>
    cd AI_TOP_100
    ```

2.  **문제 수집 (선택 사항)**
    이미 `question` 폴더에 문제가 수집되어 있지만, 다시 수집하려면 다음 명령어를 실행하세요.
    ```bash
    uv run crawl_questions.py
    python3 clean_questions.py
    ```

3.  **백엔드 서버 실행**
    ```bash
    uv run platform/backend/main.py
    ```
    서버는 `http://localhost:8000`에서 실행됩니다.

4.  **프론트엔드 서버 실행**
    새로운 터미널을 열고 다음을 실행하세요.
    ```bash
    cd platform/frontend
    npm install
    npm run dev
    ```
    브라우저에서 `http://localhost:5173`으로 접속하세요.

## 기능

-   **문제 목록 조회**: 수집된 모든 예선 및 본선 문제들을 확인할 수 있습니다.
-   **문제 풀이**: 각 문제(Q1, Q2 등)별로 나누어 코드를 작성할 수 있습니다.
-   **다국어 지원**: Python, JavaScript, C, C++, Markdown 등 다양한 언어로 답변을 작성할 수 있습니다.
-   **솔루션 저장**: 작성한 코드는 로컬의 `solve` 디렉토리에 자동으로 저장됩니다.

## 파일 구조

- `question/` — 문제 정의. 파일명 규칙: `S{시즌번호}_{예선|본선}_{인덱스}_{제목}.md`
- `source/{code}/` — 각 챌린지 자료 폴더. `{code}` 는 challenge.aitop100.org의 problem code (예: `csatmyth`, `stakeout`, `menu`).
- `solve/` — 사용자가 작성한 답안.
- `model_solutions/` — 참조용 모범 풀이.
- `REFERENCE.md` — 22개 챌린지 전체 카탈로그 (총점·문항 요약).
- `.claude/skills/fetch-brunch/`, `.claude/skills/fetch-aitop/` — 추가 콘텐츠 수집용 skill. 새 챌린지가 공개되면 이 skill을 통해 본문을 가져올 수 있습니다.

## 신규 챌린지 추가 워크플로

1. `python .claude/skills/fetch-aitop/scripts/list_problems.py --format table` — 사이트에 공개된 전체 챌린지 목록 갱신.
2. 신규 챌린지 발견 시: `question/S{n}_{round}_{idx}_{title}.md` 파일 작성, `source/{code}/README.md` 생성.
3. 본문이 필요하면 `fetch-brunch` 또는 (로그인 쿠키와 함께) `fetch-aitop`의 `fetch_detail.py`로 가져옵니다.
