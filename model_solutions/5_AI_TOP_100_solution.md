# Model Solution: Q5. Choonsik's Gourmet Menu Analysis

## Analysis
**Goal**: Extract menu items and prices from an image and perform calculations.
**Tools**: OCR (Tesseract, EasyOCR, Google Cloud Vision).

## Solution Script (Python)

```python
import pytesseract
from PIL import Image
import re

def analyze_menu(image_path):
    # 1. OCR
    text = pytesseract.image_to_string(Image.open(image_path), lang='kor+eng')
    
    # 2. Parsing Logic (Heuristic)
    # Look for patterns like "Menu Name ... 10,000"
    menu_items = []
    lines = text.split('\n')
    
    current_category = "Unknown"
    
    for line in lines:
        if "Meals" in line or "한식" in line:
            current_category = "Meals"
        elif "Sides" in line or "사이드" in line:
            current_category = "Sides"
        
        # Extract Price (numbers at end of line)
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

# 3. Answers Calculation
def solve_questions(menu_items):
    # Q1. Count 'Meals'
    meals_count = sum(1 for m in menu_items if m['category'] == 'Meals')
    print(f"Q1: {meals_count}")
    
    # Q2. Average Price of 'Sides'
    sides = [m['price'] for m in menu_items if m['category'] == 'Sides']
    if sides:
        avg_price = int(sum(sides) / len(sides))
        print(f"Q2: {avg_price}")
    
    # Q3. Highest Price
    max_price = max(m['price'] for m in menu_items)
    most_expensive = [m['name'] for m in menu_items if m['price'] == max_price]
    print(f"Q3: {', '.join(most_expensive)}")
    
    # Q4. Alcohol
    # (Requires specific keyword matching for alcohol names like 'Soju', 'Beer')
    pass
```
