"""
여권 이미지 OCR - qwen3-vl:8b 사용
30명 신청자의 여권 정보 추출
"""
import os
import json
import re
from pathlib import Path
import ollama

BASE_DIR = Path(__file__).parent
APPLICANTS_DIR = BASE_DIR / "applicants"

PASSPORT_OCR_PROMPT = """이 여권 이미지에서 다음 정보를 정확하게 추출해주세요:

1. Type (P = Passport)
2. Surname/Given Names (전체 이름)
3. Passport No. (여권번호)
4. Nationality (국적)
5. Date of Birth (생년월일, YYYY-MM-DD 형식)
6. Expiry Date (만료일, YYYY-MM-DD 형식)

JSON 형식으로만 응답하세요:
{"type": "P", "name": "이름", "passport_no": "여권번호", "nationality": "국적", "dob": "YYYY-MM-DD", "expiry_date": "YYYY-MM-DD"}

이미지에 정보가 없으면 해당 필드를 null로 표시하세요.
반드시 유효한 JSON만 출력하세요. 다른 설명은 포함하지 마세요."""


def ocr_passport(image_path: Path) -> dict:
    """VLM으로 여권 이미지 OCR"""
    try:
        response = ollama.chat(
            model='qwen3-vl:8b',
            messages=[{
                'role': 'user',
                'content': PASSPORT_OCR_PROMPT,
                'images': [str(image_path)]
            }],
            options={'temperature': 0}
        )
        content = response['message']['content']

        # JSON 추출 (```json ... ``` 또는 순수 JSON)
        json_match = re.search(r'\{[^{}]*\}', content, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        return {}
    except Exception as e:
        print(f"OCR 오류: {e}")
        return {}


def process_all_applicants():
    """모든 신청자 여권 OCR 수행"""
    results = {}

    applicant_dirs = sorted([d for d in APPLICANTS_DIR.iterdir() if d.is_dir() and d.name.startswith('applicant_')])

    for app_dir in applicant_dirs:
        app_id = app_dir.name
        images_dir = app_dir / "images"

        # 여권 페이지 2 찾기 (실제 정보 페이지)
        passport_page2 = images_dir / f"{app_id}_passport_page2.png"
        if not passport_page2.exists():
            # page1만 있는 경우
            passport_page1 = images_dir / f"{app_id}_passport_page1.png"
            if passport_page1.exists():
                passport_img = passport_page1
            else:
                print(f"{app_id}: 여권 이미지 없음")
                continue
        else:
            passport_img = passport_page2

        print(f"[{app_id}] OCR 중: {passport_img.name}...", end=" ", flush=True)

        data = ocr_passport(passport_img)
        if data:
            results[app_id] = data
            print(f"OK - {data.get('name', 'N/A')}")
        else:
            print("실패")

    return results


def main():
    print("=" * 60)
    print("여권 OCR - 30명 신청자")
    print("=" * 60)

    results = process_all_applicants()

    # 결과 저장
    output_file = BASE_DIR / "passport_ocr_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n완료: {len(results)}명 처리됨")
    print(f"결과 저장: {output_file}")

    # 요약 출력
    print("\n=== 요약 ===")
    for app_id, data in results.items():
        print(f"{app_id}: {data.get('name', 'N/A')} | {data.get('nationality', 'N/A')} | 만료: {data.get('expiry_date', 'N/A')}")


if __name__ == "__main__":
    main()
