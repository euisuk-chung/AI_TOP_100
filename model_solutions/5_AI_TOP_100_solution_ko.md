# 모범 답안: Q5. 춘식이의 미식 메뉴 분석

## 분석
**목표**: 이미지에서 메뉴 항목과 가격을 추출하고 계산을 수행합니다.
**도구**: OCR (Tesseract, EasyOCR, Google Cloud Vision).

## 풀이 스크립트 (Python)

```python
import pytesseract
from PIL import Image
import re

def analyze_menu(image_path):
    # 1. OCR
    text = pytesseract.image_to_string(Image.open(image_path), lang='kor+eng')

    # 2. 파싱 로직 (휴리스틱)
    # "메뉴명 ... 10,000"과 같은 패턴을 찾습니다
    menu_items = []
    lines = text.split('\n')

    current_category = "미분류"

    for line in lines:
        if "식사" in line or "Meals" in line or "한식" in line:
            current_category = "식사"
        elif "사이드" in line or "Sides" in line:
            current_category = "사이드"

        # 가격 추출 (줄 끝의 숫자)
        price_match = re.search(r'(\d{1,3}(,\d{3})*)', line)
        if price_match:
            price_str = price_match.group(1).replace(',', '')
            price = int(price_str)
            name = line.replace(price_match.group(0), '').strip()

            if name:
                menu_items.append({
                    "category": current_category,
                    "name": name,
                    "price": price
                })

    return menu_items

# 3. 답변 계산
def solve_questions(menu_items):
    # Q1. '식사' 메뉴 수
    meals_count = sum(1 for m in menu_items if m['category'] == '식사')
    print(f"Q1: {meals_count}")

    # Q2. '사이드' 평균 가격
    sides = [m['price'] for m in menu_items if m['category'] == '사이드']
    if sides:
        avg_price = int(sum(sides) / len(sides))
        print(f"Q2: {avg_price}")

    # Q3. 최고 가격
    max_price = max(m['price'] for m in menu_items)
    most_expensive = [m['name'] for m in menu_items if m['price'] == max_price]
    print(f"Q3: {', '.join(most_expensive)}")

    # Q4. 주류
    # (소주, 맥주 등 주류 이름에 대한 특정 키워드 매칭 필요)
    pass
```
