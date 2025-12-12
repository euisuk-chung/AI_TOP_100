# Model Solution: Q1. Choonsik Menu Analysis Challenge

## Problem Pattern

**P2. Implementation & Automation (Action)** - Implementing AI solutions as working code or workflow to solve defined problems

## Key Competencies

1. **OCR Utilization**: Accurately extract text (menu, prices) from images
2. **Data Cleaning**: Process OCR noise and convert to structured data
3. **Calculation Verification**: Perform accurate calculations based on extracted data
4. **Implicit Verification**: Require verifiable answers like item count, average price

## Why Can't This Be Solved with a Single Click?

- Simply showing menu image to AI and saying "analyze it" may result in **OCR errors**
- Korean menu names, special fonts, decorative elements make **perfect recognition difficult**
- Category classification (meals/sides/alcohol) requires **context understanding**
- Calculation results need **human verification**

---

## Recommended Approach

### Step 1: Human Analysis

- Understand overall structure of menu image (sections, layout)
- Determine if image preprocessing is needed for OCR
- Define category classification criteria (meals, sides, beverages, alcohol)

### Step 2: AI Collaboration

```text
Example Prompt:
"Extract all menu items and prices from this menu image.
Format the results as JSON:
{
  'category': 'Meals/Sides/Drinks/Alcohol',
  'name': 'Menu name',
  'price': price(number)
}

Category criteria:
- Meals: Rice, noodles, stews - main dishes
- Sides: Side dishes, accompaniments
- Drinks: Non-alcoholic beverages
- Alcohol: Soju, beer, makgeolli, etc."
```

### Step 3: Human Verification

1. **Compare** AI-extracted menu list with original image
2. **Manually correct** missing items or incorrectly recognized prices
3. **Double-check calculations** (totals, averages) with calculator

---

## Solution Script (Python)

```python
import pytesseract
from PIL import Image
import re

def analyze_menu(image_path):
    """Extract menu information from menu image"""

    # 1. Perform OCR
    text = pytesseract.image_to_string(Image.open(image_path), lang='kor+eng')

    # 2. Parsing Logic
    menu_items = []
    lines = text.split('\n')

    current_category = "Uncategorized"

    # Category keywords
    category_keywords = {
        "Meals": ["Meals", "Rice", "Noodles", "Stew", "Set"],
        "Sides": ["Sides", "Side Dish"],
        "Drinks": ["Drinks", "Coffee", "Tea", "Beverage"],
        "Alcohol": ["Alcohol", "Soju", "Beer", "Wine"]
    }

    for line in lines:
        # Detect category
        for cat, keywords in category_keywords.items():
            if any(kw in line for kw in keywords):
                current_category = cat
                break

        # Extract price (number pattern at end of line)
        price_match = re.search(r'(\d{1,3}(,\d{3})*)\s*$', line)
        if price_match:
            price_str = price_match.group(1).replace(',', '')
            price = int(price_str)
            name = line.replace(price_match.group(0), '').strip()

            if name and len(name) > 1:
                menu_items.append({
                    "category": current_category,
                    "name": name,
                    "price": price
                })

    return menu_items
```

---

### Q1. Cooking Method Analysis

**Approach**: Extract side dishes from the designated week's lunch menus and count items ending with specific cooking methods (braised, stir-fried, seasoned, grilled).

**Guide**:

1. Collect menu images for the week (Mon-Fri)
2. Extract side dish lists from Korean A, Korean B, Popup A, Popup B, Western corners
3. Check if side dish name ends with cooking method keywords
4. Count each cooking method and sort in descending order

**Analysis Results**:

| Cooking Method | Count |
|----------------|-------|
| Braised | 12 |
| Stir-fried | 9 |
| Seasoned | 7 |
| Grilled | 4 |

**Answer**: **4. Braised > Stir-fried > Seasoned > Grilled**

---

### Q2. January Calorie Ranking

**Approach**: Extract calorie information for all lunch menus and calculate averages by corner.

**Guide**:

1. Extract menus and calories from all January weeks
2. Collect calorie values by corner and calculate averages
3. Sort by average calories in descending order

**Analysis Results**:

| Corner | Average Calories |
|--------|------------------|
| Western | ~920kcal |
| Popup B | ~880kcal |
| Korean A | ~850kcal |
| Korean B | ~780kcal |
| Popup A | ~720kcal |

**Answer**: **4. Western > Popup B > Korean A > Korean B > Popup A**

---

### Q3. Regional Specialty Menus

**Approach**: Extract country/city/region names from all menu names and select regions appearing 2+ times.

**Guide**:

1. Collect complete menu name list (lunch, lunch takeout, dinner, dinner takeout)
2. Match against known region name list
3. Count occurrences of each region
4. Select regions appearing 2+ times

**Analysis Results**:

| Region | Occurrences |
|--------|-------------|
| Thailand | 3 times |
| Nagasaki | 2 times |
| Andong | 2 times |
| Vietnam | 1 time |
| Jeonju | 1 time |

**Answer**: **1. Thailand, 3. Nagasaki, 4. Andong** (multiple selection)

---

### Q4. Menu Calorie Comparison

**Approach**: Find and compare calories for the 5 specified menus.

**Guide**:

1. Search for menu names in January-February menu boards
2. Extract calorie value for each menu
3. Sort by calories in descending order

**Analysis Results**:

| Menu Name | Calories |
|-----------|----------|
| Homemade Namsan Pork Cutlet | 950kcal |
| Malatang Noodles | 880kcal |
| Tonkotsu Ramen | 820kcal |
| Tantan Noodles | 750kcal |
| Denkasu Tteokbokki | 680kcal |

**Answer**: **4. Homemade Namsan Pork Cutlet > Malatang > Tonkotsu Ramen > Tantan > Denkasu Tteokbokki**

---

### Q5. February Monthly Diet Optimization Challenge

**Approach**: Find the corner combination where lunch+dinner totals closest to 1,550kcal for each day, with Fridays selecting the lowest calorie lunch corner.

**Guide**:

1. Collect calorie data by corner for each February date
2. Mon-Thu: Select combination with total closest to 1,550kcal
3. Friday: Select lowest calorie lunch corner (no dinner)
4. Output in JSON format

**Answer** (JSON format):

```json
{
  "2/3": {"lunch": "Salad", "dinner": "Korean B"},
  "2/4": {"lunch": "Vegan", "dinner": "Salad"},
  "2/5": {"lunch": "Korean A", "dinner": "Korean B"},
  "2/6": {"lunch": "Popup A", "dinner": "Burger&Deli"},
  "2/7": {"lunch": "Salad"},
  "2/10": {"lunch": "Western", "dinner": "Korean B"},
  "2/11": {"lunch": "Korean B", "dinner": "Salad"},
  "2/12": {"lunch": "Popup B", "dinner": "Korean B"},
  "2/13": {"lunch": "Rice&Noodle", "dinner": "Burger&Deli"},
  "2/14": {"lunch": "Vegan"},
  "2/17": {"lunch": "Korean A", "dinner": "Korean B"},
  "2/18": {"lunch": "Western", "dinner": "Salad"},
  "2/19": {"lunch": "Popup A", "dinner": "Korean B"},
  "2/20": {"lunch": "Burger&Deli", "dinner": "Burger&Deli"},
  "2/21": {"lunch": "Salad"},
  "2/24": {"lunch": "Korean B", "dinner": "Korean B"},
  "2/25": {"lunch": "Popup B", "dinner": "Salad"},
  "2/26": {"lunch": "Western", "dinner": "Korean B"},
  "2/27": {"lunch": "Vegan", "dinner": "Burger&Deli"},
  "2/28": {"lunch": "Rice&Noodle"}
}
```

---

## Key Lesson

> "Extracting data from images requires both **AI's OCR capability** and **human verification**. Especially with decorative elements like menu boards, **human checking and correction** is essential."

This problem demonstrates OCR technology limitations and the importance of data cleaning. The habit of **not blindly trusting AI results and verifying** is crucial.
