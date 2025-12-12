# 모범 답안: Q1. 춘식도락 메뉴 분석

## 출제 의도

### 문제 패턴

**P2. 구현 및 자동화 (Action)** - 정의된 문제를 해결하기 위해 AI 솔루션을 실제 작동하는 코드나 워크플로로 구현

### 핵심 측정 역량

1. **OCR 활용 능력**: 이미지에서 텍스트(메뉴, 가격)를 정확히 추출
2. **데이터 정제 능력**: OCR 결과의 노이즈를 처리하고 구조화된 데이터로 변환
3. **계산 검증**: 추출된 데이터를 바탕으로 정확한 계산 수행
4. **암묵적 검증 유도**: 메뉴 항목 수, 평균 가격 등 검증 가능한 정답 요구

### 왜 '딸깍'으로 풀리지 않는가?

- AI에게 메뉴 이미지를 보여주고 "분석해줘"라고 하면 **OCR 오류 발생 가능**
- 한글 메뉴명, 특수 폰트, 장식적 요소로 인해 **완벽한 인식이 어려움**
- 카테고리 분류(식사/사이드/주류)는 **문맥 이해 필요** - AI가 임의로 분류할 수 있음
- 계산 결과가 맞는지 **사람이 직접 검산**해야 함

### 난이도 구조

- **Q1 (Easy)**: 메뉴 수 세기 - 기본적인 카테고리 분류
- **Q2 (Medium)**: 평균 가격 계산 - 데이터 추출 + 계산
- **Q3 (Easy)**: 최고가 메뉴 - 단순 비교
- **Q4 (Hard)**: 주류 식별 - 도메인 지식 필요 (킬러 문항)

---

## 권장 접근법

### 1단계: 사람의 분석

- 메뉴판 이미지의 전체 구조 파악 (섹션, 레이아웃)
- OCR이 잘 인식할 수 있도록 이미지 전처리 필요 여부 판단
- 카테고리 분류 기준 정의 (식사, 사이드, 주류의 구분)

### 2단계: AI와의 협업

```text
프롬프트 예시:
"이 메뉴판 이미지에서 모든 메뉴 항목과 가격을 추출해줘.
결과를 다음 형식의 JSON으로 정리해줘:
{
  'category': '식사/사이드/음료/주류',
  'name': '메뉴명',
  'price': 가격(숫자)
}

카테고리 분류 기준:
- 식사: 밥, 면, 찌개 등 주요리
- 사이드: 반찬, 곁들임 요리
- 음료: 비알콜 음료
- 주류: 소주, 맥주, 막걸리 등"
```

### 3단계: 사람의 검증

1. AI가 추출한 메뉴 목록을 **원본 이미지와 대조**
2. 누락된 항목이나 잘못 인식된 가격 **수동 교정**
3. 계산 결과(합계, 평균)를 **직접 계산기로 검산**

---

## 풀이 스크립트 (Python)

```python
import pytesseract
from PIL import Image
import re

def analyze_menu(image_path):
    """메뉴판 이미지에서 메뉴 정보 추출"""

    # 1. OCR 수행
    text = pytesseract.image_to_string(Image.open(image_path), lang='kor+eng')

    # 2. 파싱 로직
    menu_items = []
    lines = text.split('\n')

    current_category = "미분류"

    # 카테고리 키워드 정의
    category_keywords = {
        "식사": ["식사", "밥", "면", "찌개", "탕", "정식", "Meals"],
        "사이드": ["사이드", "반찬", "곁들임", "Sides"],
        "음료": ["음료", "커피", "차", "Drinks"],
        "주류": ["주류", "소주", "맥주", "막걸리", "와인", "Alcohol"]
    }

    for line in lines:
        # 카테고리 감지
        for cat, keywords in category_keywords.items():
            if any(kw in line for kw in keywords):
                current_category = cat
                break

        # 가격 추출 (줄 끝의 숫자 패턴)
        price_match = re.search(r'(\d{1,3}(,\d{3})*)\s*원?$', line)
        if price_match:
            price_str = price_match.group(1).replace(',', '')
            price = int(price_str)
            name = line.replace(price_match.group(0), '').strip()

            if name and len(name) > 1:  # 의미 있는 이름인지 확인
                menu_items.append({
                    "category": current_category,
                    "name": name,
                    "price": price
                })

    return menu_items

def solve_questions(menu_items):
    """추출된 메뉴 데이터로 문제 풀이"""

    # Q1. '식사' 메뉴 수
    meals = [m for m in menu_items if m['category'] == '식사']
    print(f"Q1. 식사 메뉴 수: {len(meals)}")

    # Q2. '사이드' 평균 가격
    sides = [m['price'] for m in menu_items if m['category'] == '사이드']
    if sides:
        avg_price = sum(sides) // len(sides)  # 정수 나눗셈
        print(f"Q2. 사이드 평균 가격: {avg_price}원")

    # Q3. 최고가 메뉴
    if menu_items:
        max_price = max(m['price'] for m in menu_items)
        most_expensive = [m['name'] for m in menu_items if m['price'] == max_price]
        print(f"Q3. 최고가 메뉴: {', '.join(most_expensive)} ({max_price}원)")

    # Q4. 주류 메뉴
    alcohol = [m for m in menu_items if m['category'] == '주류']
    print(f"Q4. 주류 메뉴: {[m['name'] for m in alcohol]}")

# 사용 예시
# menu_data = analyze_menu("menu_image.png")
# solve_questions(menu_data)
```

---

## 구체적인 답변 가이드

### Q1. 식사 메뉴 수

**접근법**: OCR로 추출한 후, "식사" 섹션에 해당하는 항목 수 세기

**검증**: 원본 이미지에서 직접 세어서 대조

### Q2. 사이드 평균 가격

**접근법**: 사이드 카테고리 항목들의 가격 합계 ÷ 항목 수

**검증**: 계산기로 직접 검산

### Q3. 최고가 메뉴

**접근법**: 모든 메뉴 가격을 비교하여 최대값 찾기

**검증**: 가격이 비슷한 메뉴들 재확인

### Q4. 주류 식별

**접근법**: 한국 주류 키워드(소주, 맥주, 막걸리, 와인 등)로 필터링

**주의**: 음료와 주류 구분 필요 - 도메인 지식 활용

---

## 핵심 교훈

> "이미지에서 데이터를 추출하는 작업은 **AI의 OCR 능력**과 **사람의 검수**가 함께해야 정확하다. 특히 메뉴판처럼 장식적 요소가 많은 이미지에서는 **사람이 직접 확인하고 교정**하는 과정이 필수다."

이 문제는 OCR 기술의 한계와 데이터 정제의 중요성을 보여줍니다. AI가 추출한 결과를 **무조건 신뢰하지 않고 검증**하는 습관이 중요합니다.
