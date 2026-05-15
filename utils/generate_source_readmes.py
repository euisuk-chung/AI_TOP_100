#!/usr/bin/env python3
"""Generate `source/<code>/README.md` for every challenge.

Run once from the repo root:
    python utils/generate_source_readmes.py
"""
from __future__ import annotations

import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (code, title, zip/data-name, season-tag, data summary)
CHALLENGES: list[tuple[str, str, str, str, str]] = [
    # Season 1 (#1)
    ("menu", "춘식도락메뉴 분석 챌린지", "menu_challenge", "S1 예선",
     "카카오 구내식당 춘식도락의 메뉴 이미지 모음. 이 폴더에는 이미 menu_challenge/ 가 들어있습니다."),
    ("crypt", "고대 유적의 비밀: 이상한 코드 석판", "ai_top_100_crypto.png", "S1 예선",
     "코드 석판 이미지 1장."),
    ("ageofai", "The Age of AI: 영상 팩트 체크", "ai_top_100_ageofai.txt", "S1 예선",
     "YouTube 영상 5편의 링크 목록."),
    ("modeling", "전투 없이 예측하는 시뮬레이션의 힘", "ai_top_100_modeling.zip", "S1 예선",
     "`train_battles.json` (29,000건) / `test_battles.json` (500건)."),
    ("textfinder", "PDF 속 스텔스 텍스트 추적기", "ai_top_100_textfinder.zip", "S1 예선",
     "PDF 4개 (pdf_1 ~ pdf_4)."),
    ("immigration", "AI 입국 심사관", "ai_top_100_final_immigration.zip", "S1 본선",
     "신청자 30명 서류, `inspection_rules.txt`, `atlantis_world_map.png`."),
    ("montage", "몽타주를 그려라", None, "S1 본선",
     "API 기반 챌린지. 별도 다운로드 자료가 없으며, 사이트의 몽타주 제출 API를 통해 진행합니다."),
    # Season 2 (#2)
    ("handover", "인수인계 자료 작성", "ai_top_100_final_handover.zip", "S2 본선",
     "이메일/일정/메모/통화내역, `template.md`. (음성 zip 비밀번호: 0529)"),
    ("cooking", "스파이의 요리코드", "ai_top_100_final_cooking.zip", "S2 본선",
     "요리코드 1.txt ~ 5.txt, `cookingguide.png`."),
    # Season 3 (#3)
    ("news", "뉴스 속 혁신가를 발굴하라", "ai_top_100_final_news.txt", "S3 본선",
     "뉴스 기사 588건의 URL 목록."),
    ("ascii", "고대 유적의 비밀 II: 아스키 미로 탈출", "ai_top_100_final_ascii.zip", "S3 본선",
     "`q1/image.png`, `q2/` 디렉토리 40개, `q3/` 구멍난 이미지 + 조각 1,000개."),
    ("parking", "주차의 달인", "ai_top_100_final_parking.zip", "S3 본선",
     "`stage_1` ~ `stage_4`, `simulator.py`, `render_stage.py`."),
    # Season 4 (CAMPUS 예선)
    ("csat", "2026 수능, 그날의 대화", "ai_top_100_campus_csat.zip", "S4 CAMPUS 예선",
     "2026 수능 문제지·정답, 대화 기록 4건, `subject_list.txt`."),
    ("art-detective", "디지털 아트 감정사: AI 위작을 찾아라", "ai_top_100_campus_art-detective.zip", "S4 CAMPUS 예선",
     "이미지 100장, `artists.txt`, `vermeer_titles.txt`, `vermeer_museums.txt`."),
    ("freerider", "프리라이더를 찾아라", "ai_top_100_campus_freerider.zip", "S4 CAMPUS 예선",
     "Team A~D의 카톡 스크린샷·발표자료·자료, `CONTRIBUTION_SCORE.txt`."),
    ("webqa", "웹사이트 버그 찾기", "ai_top_100_campus_webqa.zip", "S4 CAMPUS 예선",
     "홈페이지 소스코드 `site/`, `spec.pdf`."),
    ("newspaper", "1906, 오늘 한성은", "ai_top_100_campus_newspaper.jpg", "S4 CAMPUS 예선",
     "1906년 3월 14일자 신문 이미지 1장."),
    # Season 5 (CAMPUS 본선)
    ("csatmyth", "수능 경향 분석", "ai_top_100_campus_final_csatmyth.zip", "S5 CAMPUS 본선",
     "`csat_dataset` (2022~2026 수능 원본) / `statistics` (1994~2026 평가원 통계)."),
    ("stakeout", "AI 수사관: 잠복 근무", "ai_top_100_campus_final_stakeout.zip", "S5 CAMPUS 본선",
     "오디오 100개, `suspect_db.csv` (1,000명), CCTV/SNS 이미지, 헥스 그리드 지도."),
    ("startup", "스타트업 창업 여정: 투자의 조건", "ai_top_100_campus_final_startup.zip", "S5 CAMPUS 본선",
     "과거 심사 19건, 강의 과제 6건, 피치 주제 10개."),
    ("webnovel", "웹소설 플랫폼 복구하기", "ai_top_100_campus_final_webnovel.zip", "S5 CAMPUS 본선",
     "`index.html` 기반 웹소설 사이트 일체."),
    ("newspaper-final", "號外요 號外! 시간 여행자가 나타났어요", "ai_top_100_campus_final_newspaper.zip", "S5 CAMPUS 본선",
     "`황성신문.jpg`, `독립신문.csv` (2,000건)."),
]


def render(code: str, title: str, zip_name: str | None, season: str, summary: str) -> str:
    download_section = (
        f"`{zip_name}`" if zip_name else "별도 다운로드 자료 없음 (사이트 API 사용)"
    )
    return textwrap.dedent(
        f"""\
        # {title}

        - **시즌**: {season}
        - **챌린지 코드**: `{code}`
        - **사이트**: https://challenge.aitop100.org/problem/{code}

        ## 자료

        다운로드: {download_section}

        ## 포함 데이터

        {summary}

        ## 사용 방법

        1. challenge.aitop100.org 로그인 후 자료 탭에서 압축 파일을 받습니다.
        2. 이 폴더(`source/{code}/`)에 압축을 풀어 배치합니다.
        3. `question/` 의 해당 문제 markdown에서 Source 링크가 이 폴더를 가리킵니다.
        """
    )


def main() -> int:
    written = 0
    for code, title, zip_name, season, summary in CHALLENGES:
        target = ROOT / "source" / code / "README.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(code, title, zip_name, season, summary), encoding="utf-8")
        written += 1
    print(f"wrote {written} README files under source/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
