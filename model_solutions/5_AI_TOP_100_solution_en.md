# Model Solution: Q5. PDF Stealth Text Tracker

## Analysis
The problem asks to find hidden text in PDF files.
**Techniques**:
1.  **Hidden Layer/White Text**: Extract all text using a library.
2.  **Image Steganography**: Analyze images extracted from PDF.

## Solution Script (Python)

```python
import pdfplumber
import re

def find_hidden_text(pdf_path):
    hidden_texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 1. Extract all text (including white/hidden text)
            text = page.extract_text()
            
            # 2. Filter for specific patterns (e.g., "Total 14 words")
            # This part requires manual inspection or specific heuristics
            print(f"--- Page {page.page_number} ---")
            print(text)
            
            # 3. Check for white text (if library supports color extraction)
            for char in page.chars:
                if char['non_stroking_color'] == (1, 1, 1): # White in RGB
                    print(f"Found white text: {char['text']}")

    return hidden_texts

# Usage
# find_hidden_text("pdf_1.pdf")
```

## Specific Answers (Hypothetical)

-   **Q1 (pdf_1.pdf)**: Likely text hidden behind an image or same color as background. `pdfplumber` or `pdfminer.six` can extract it.
-   **Q2 (pdf_2.pdf)**: "Small white text". The script above checking for `(1,1,1)` color or font size `< 1` would find it.
-   **Q3 (pdf_3.pdf)**: "Invisible text below visible layer". Standard text extraction usually grabs this.
-   **Q4 (pdf_4.pdf)**: "Lyrics of famous English song". Extract all text and look for song lyrics (e.g., "Never gonna give you up", "Bohemian Rhapsody").
