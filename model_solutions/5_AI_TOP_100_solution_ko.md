# 모범 답안: Q5. PDF 속 스텔스 텍스트 추적기

## 출제 의도

### 문제 패턴

**P1. 분석 및 정의 (Insight)** - 정답이 없는 복합 데이터 속에서 의미 있는 '문제'나 '기회'를 스스로 정의하고 발견

### 핵심 측정 역량

1. **숨겨진 정보 탐지 능력**: PDF 내 다양한 방식으로 숨겨진 텍스트를 찾는 기술적 이해
2. **다양한 도구 활용**: PDF 분석 라이브러리, OCR, 텍스트 추출 도구 등 적절한 도구 선택
3. **암묵적 검증 유도**: 노래 가사, 단어 수 등 검증 포인트를 통해 정답 확인

### 왜 '딸깍'으로 풀리지 않는가?

- PDF에 텍스트를 숨기는 방법이 **다양함** (흰색 텍스트, 이미지 뒤, 레이어, 메타데이터 등)
- AI가 PDF를 직접 분석하기 어려움 - **사람이 적절한 도구를 선택**해야 함
- 주관식 답변이므로 AI의 할루시네이션 가능성 있음 - **검증 필수**

### 난이도 구조

- **Q1-Q3 (Medium)**: 일반적인 PDF 텍스트 추출 도구로 발견 가능
- **Q4 (Hard)**: "유명한 영어 노래 가사"라는 힌트 제공 - 검증 포인트

---

## 권장 접근법

### 1단계: 사람의 분석

- PDF에 텍스트를 숨기는 일반적인 방법들 파악
  - 흰색 텍스트 (배경과 같은 색)
  - 매우 작은 폰트 크기
  - 이미지 레이어 아래
  - PDF 메타데이터
  - 주석(Annotation)

### 2단계: AI와의 협업

```text
프롬프트 예시:
"PDF에서 숨겨진 텍스트를 찾는 Python 스크립트를 작성해줘.
다음 방법들을 시도해봐:
1. pdfplumber로 모든 텍스트 추출
2. 텍스트의 색상 정보 확인 (흰색 텍스트 탐지)
3. 폰트 크기가 매우 작은 텍스트 탐지
4. PyMuPDF로 레이어별 텍스트 추출"
```

### 3단계: 사람의 검증

1. 추출된 텍스트가 문제의 힌트와 일치하는지 확인 (예: "14단어", "노래 가사")
2. 여러 도구로 교차 검증
3. 결과가 의미 있는 문장인지 확인

---

## 풀이 스크립트 (Python)

```python
import pdfplumber
import fitz  # PyMuPDF

def find_hidden_text_pdfplumber(pdf_path):
    """pdfplumber를 사용한 텍스트 추출"""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            # 모든 텍스트 추출
            text = page.extract_text()
            print(f"--- 페이지 {page.page_number} (일반 텍스트) ---")
            print(text)

            # 흰색 텍스트 탐지
            for char in page.chars:
                color = char.get('non_stroking_color')
                if color == (1, 1, 1) or color == (1.0, 1.0, 1.0):
                    print(f"흰색 텍스트 발견: {char['text']}")

                # 매우 작은 폰트 탐지
                if char.get('size', 12) < 2:
                    print(f"작은 폰트 텍스트: {char['text']}")

def find_hidden_text_pymupdf(pdf_path):
    """PyMuPDF를 사용한 텍스트 추출"""
    doc = fitz.open(pdf_path)
    for page_num, page in enumerate(doc):
        # 텍스트 블록 추출
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"]
                        color = span.get("color", 0)
                        size = span.get("size", 12)

                        # 흰색(0xFFFFFF) 또는 매우 작은 텍스트
                        if color == 16777215 or size < 2:
                            print(f"숨겨진 텍스트: {text}")

# 사용법
# find_hidden_text_pdfplumber("pdf_1.pdf")
# find_hidden_text_pymupdf("pdf_1.pdf")
```

---

## 구체적인 답변 가이드

### Q1 (pdf_1.pdf)

**접근법**: 이미지 뒤에 숨겨지거나 배경과 같은 색상의 텍스트일 가능성이 높습니다.

**도구**: `pdfplumber` 또는 `pdfminer.six`로 추출

### Q2 (pdf_2.pdf)

**접근법**: "작은 흰색 텍스트" - 폰트 크기가 매우 작거나 흰색인 텍스트

**도구**: 위 스크립트에서 `(1,1,1)` 색상 또는 폰트 크기 `< 2`를 확인

### Q3 (pdf_3.pdf)

**접근법**: "보이는 레이어 아래의 보이지 않는 텍스트"

**도구**: 일반적인 텍스트 추출로 보통 가져올 수 있음

### Q4 (pdf_4.pdf)

**접근법**: "유명한 영어 노래 가사"라는 힌트 활용

**검증 방법**:

1. 추출된 텍스트를 AI에게 "이게 어떤 노래 가사인지 알려줘"라고 질문
2. 유명한 노래 가사인지 확인 (예: "Never gonna give you up", "Bohemian Rhapsody" 등)

---

## 핵심 교훈

> "숨겨진 정보를 찾는 것은 **다양한 도구와 방법을 시도**하는 것이다. AI는 코드 작성을 도와주지만, **어떤 방법을 시도할지**는 사람이 결정한다."

이 문제는 주어진 힌트(단어 수, 노래 가사)를 활용하여 **AI 결과물을 검증**하는 능력을 측정합니다. 주관식 문제에서 AI의 할루시네이션을 방지하려면 **교차 검증이 필수**입니다.
