# 모범 답안: Q3. PDF 속 텍스트 추적

## 분석
이 문제는 PDF 파일에서 숨겨진 텍스트를 찾는 것입니다.
**기법**:
1.  **숨겨진 레이어/흰색 텍스트**: 라이브러리를 사용하여 모든 텍스트를 추출합니다.
2.  **이미지 스테가노그래피**: PDF에서 추출한 이미지를 분석합니다.

## 풀이 스크립트 (Python)

```python
import pdfplumber
import re

def find_hidden_text(pdf_path):
    hidden_texts = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 1. 모든 텍스트 추출 (흰색/숨겨진 텍스트 포함)
            text = page.extract_text()

            # 2. 특정 패턴 필터링 (예: "총 14단어")
            # 이 부분은 수동 검사 또는 특정 휴리스틱이 필요합니다
            print(f"--- 페이지 {page.page_number} ---")
            print(text)

            # 3. 흰색 텍스트 확인 (라이브러리가 색상 추출을 지원하는 경우)
            for char in page.chars:
                if char['non_stroking_color'] == (1, 1, 1): # RGB에서 흰색
                    print(f"흰색 텍스트 발견: {char['text']}")

    return hidden_texts

# 사용법
# find_hidden_text("pdf_1.pdf")
```

## 구체적인 답변 (가설)

-   **Q1 (pdf_1.pdf)**: 이미지 뒤에 숨겨지거나 배경과 같은 색상의 텍스트일 가능성이 높습니다. `pdfplumber` 또는 `pdfminer.six`로 추출할 수 있습니다.
-   **Q2 (pdf_2.pdf)**: "작은 흰색 텍스트". 위 스크립트에서 `(1,1,1)` 색상 또는 글꼴 크기 `< 1`을 확인하면 찾을 수 있습니다.
-   **Q3 (pdf_3.pdf)**: "보이는 레이어 아래의 보이지 않는 텍스트". 일반적인 텍스트 추출로 보통 이것을 가져옵니다.
-   **Q4 (pdf_4.pdf)**: "유명한 영어 노래 가사". 모든 텍스트를 추출하고 노래 가사를 찾습니다 (예: "Never gonna give you up", "Bohemian Rhapsody").
