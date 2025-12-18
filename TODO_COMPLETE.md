# AI TOP 100 - 전체 TODO

**작성일**: 2025-12-19
**총 문제 수**: 9개 (예선 5개 + 본선 4개)

---

## 해결 현황 요약

| 문제 | 상태 | 세부 진행률 | 필요 작업 |
|------|------|-------------|-----------|
| Q1 춘식도락 메뉴 분석 | ✅ 완료 | 5/5 | - |
| Q2 고대 유적의 비밀 | ✅ 완료 | 3/3 | - |
| Q3 영상 팩트 체크 | ⏳ 부분 | 3/7 | VLM 영상 분석 |
| Q4 전투 게임 시뮬레이션 | ✅ 완료 | 6/6 | - |
| Q5 PDF 속 텍스트 추적 | ⏳ 부분 | 3/4 | 5번째 노래 찾기 |
| Q6 AI 입국 심사관 | ❌ 미해결 | 0/1 | 이미지 PDF OCR |
| Q7 몽타주를 그려라 | ❌ 미해결 | 0/1 | API 제출 |
| Q8 인수인계 | ⏳ 부분 | 2/4 | 음성 Transcript |
| Q9 스파이의 요리코드 | ❌ 미해결 | 0/5 | 인터프리터 구현 |

---

## Q3. 영상 팩트 체크 (예선) - 3/7

**Source**: YouTube 영상 5편 (The Age of AI 시리즈)

### 해결된 문항
| 문항 | 답안 | 출처 |
|------|------|------|
| Q3-2 | `Who are you talking about?` | AI를 통한 치유.txt line 435 |
| Q3-3 | `lap 318` (피트스톱 시간 확인 필요) | AI를 이용해 더 나은 인간 만들기.txt line 374 |
| Q3-5 | Long Beach, Waterloo (Canada), San Francisco | 로봇이 내 일자리를 빼앗을까.txt |

### 미해결 문항 (VLM 필요)
| 문항 | 필요한 정보 | 힌트 |
|------|-------------|------|
| Q3-1 | 킹콩/아바타 안면 작업자가 마신 음료 | Mark Sagar 인터뷰 장면 |
| Q3-4 | Bobo 역 배우 과거 직업 | John Hennigan - 추정: 프로레슬러 (WWE) |
| Q3-6 | 얼굴 마커 갯수 (콧등, 양쪽 눈, 눈썹) | 얼굴 캡처 장면 |
| Q3-7 | 사실 확인 복수 선택 | Transcript 검증 필요 |

### Transcript 파일 위치
```
d:\repo\AI_TOP_100\source\q3\transcript\
├── 적정선은 어디인가.txt
├── AI를 통한 치유.txt
├── AI를 이용해 더 나은 인간 만들기.txt
├── 사랑, 예술 그리고 이야기를 이해하다.txt
└── 로봇이 내 일자리를 빼앗을까.txt
```

### 다음 단계
1. [ ] Ollama 설치 + Qwen2-VL/LLaVA 모델 다운로드
2. [ ] YouTube 영상 다운로드 → 프레임 추출
3. [ ] VLM으로 Q1, Q4, Q6 시각 분석
4. [ ] Q7 문제 보기 확인 후 Transcript와 대조

### VLM 사용 코드
```python
# 영상 프레임 추출
import cv2
import os

def extract_frames(video_path, output_dir, interval_sec=1):
    os.makedirs(output_dir, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = int(fps * interval_sec)
    frame_count = saved_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        if frame_count % frame_interval == 0:
            cv2.imwrite(f"{output_dir}/frame_{saved_count:04d}.jpg", frame)
            saved_count += 1
        frame_count += 1
    cap.release()

# Ollama 이미지 분석
import ollama, base64

def analyze_image(image_path, prompt):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    response = ollama.chat(
        model="llava:13b",
        messages=[{"role": "user", "content": prompt, "images": [image_data]}]
    )
    return response["message"]["content"]
```

---

## Q5. PDF 속 텍스트 추적 (예선) - 3/4

**Source**: pdf_1~4.pdf

### 해결된 문항
| 문항 | 답안 |
|------|------|
| Q5-1 | pdf_1 배경색 숨김 14단어 (확인 필요) |
| Q5-2 | pdf_2 흰색 작은 텍스트 11단어 (확인 필요) |
| Q5-3 | pdf_3 레이어 아래 텍스트 5단어 (확인 필요) |

### 미해결 문항
| 문항 | 필요 정보 | 현황 |
|------|-----------|------|
| Q5-4 | pdf_4 숨겨진 노래 5곡 | 4곡 발견 |

### 발견된 노래 (4/5)
1. Twinkle twinkle little star (Page 14)
2. Jingle bells (Page 37)
3. Oh Danny boy (Page 109)
4. Row row row your boat (Page 162)
5. ??? (미발견)

### 다음 단계
1. [ ] pdf_4에서 5번째 숨겨진 노래 찾기
2. [ ] Q5-1~3 답안 최종 검증

---

## Q6. AI 입국 심사관 (본선) - 0/1

**Source**: source/q6 (applicants/, inspection_rules.txt)
**문제**: 30명 신청자 심사 → JSON 결과 제출
**심사일**: 2025-11-22

### 현황
- ✅ PDF → 이미지 변환 완료 (197개 이미지)
- ✅ 25개 규칙 파싱 완료
- ✅ OCR 스크립트 작성됨: `run_deepseek_ocr.py`
- ⏳ **대기**: DeepSeek-OCR로 텍스트 추출 (GPU PC 필요)
- **문제점**: 현재 results.json에서 30명 전원 Deny (Rule 8 이름 불일치) - 재검증 필요

### 폴더 구조
```
source/q6/
├── applicants/
│   ├── applicant_001/
│   │   ├── *.pdf (원본 서류)
│   │   ├── images/ (변환된 이미지 - 완료)
│   │   └── ocr_content.txt (추출될 텍스트)
│   └── ... (총 30명)
├── inspection_rules.txt (25개 심사 규칙)
├── atlantis_world_map.md (국가별 비자 정보)
├── immigration_check.py (심사 스크립트)
├── run_deepseek_ocr.py (OCR 스크립트)
└── results.json (현재 결과 - 재검증 필요)
```

### 25개 심사 규칙 요약
- 1-7: 서류 미제출 (여권, 비자, 입국신고서, 항공권, 재정증명서, 건강증명서, 세관신고서)
- 8-9: 일관성 오류 (이름/여권번호 불일치)
- 10-15: 유효성 오류 (만료, 기간 초과, 사진 미부착)
- 16-20: 비자 관련 (목적, 타입, 체류기간, 입국횟수, 발급지)
- 21-25: 건강/재정 (발열, COVID, 재정부족, 백신, 금지품목)

### 무비자 협정국
| 국가 | 허용 기간 |
|------|-----------|
| Kingdom of Neverland | 30일 |
| Federation of Serenia | 60일 |
| Republic of Valeria | 90일 |

### 비자 필요 국가
- Empire of Dragonia, Republic of Crystalline, United States of Eldorado
- Kingdom of Avalon, Mystical Islands

### GPU PC에서 실행 방법
```bash
# 필요 패키지
pip install transformers torch pymupdf

# OCR 실행 (이미지는 이미 변환됨)
cd d:/repo/AI_TOP_100/source/q6
python run_deepseek_ocr.py --step 2
```

### 다음 단계
1. [ ] GPU PC에서 `python run_deepseek_ocr.py --step 2` 실행
2. [ ] OCR 결과 확인 (각 applicant 폴더의 ocr_content.txt)
3. [ ] `immigration_check.py` 수정 (OCR 결과 활용)
4. [ ] VISA_FREE_COUNTRIES 딕셔너리 설정
5. [ ] 30명 심사 결과 재검증
6. [ ] JSON 형식으로 최종 답안 생성

### 제출 형식
```json
[
  {"id": "applicant_001", "answer": "Approve"},
  {"id": "applicant_002", "answer": "Deny", "reason": 3}
]
```

---

## Q7. 몽타주를 그려라 (본선) - 0/1

**문제**: 범인 몽타주 생성 → API 제출 → 유사도 피드백 → 반복 개선

### 목격자 묘사
> "30대 정도의 남성에 눈이 크고 아몬드 모양의 깊고 진한 눈, 길고 곧게 뻗었지만 좌우 폭은 넓지 않은 코, 부드러운 미소를 가졌으며 양 옆으로 길지 않은 입술"

### 제약 조건
- 1024x1024 해상도
- PNG/JPEG, 10MB 이하
- Rate limit: 1분당 1회

### 다음 단계
1. [ ] API 엔드포인트 확인
2. [ ] DALL-E 또는 Stable Diffusion으로 초기 몽타주 생성
3. [ ] 피드백 기반 프롬프트 개선 반복

---

## Q8. 인수인계 (본선) - 2/4

**Source**: source/q8 (메일, 캘린더, 메모, 책상, 통화)

### 해결된 문항
| 문항 | 답안 | 출처 |
|------|------|------|
| Q8-2 | **4곳** (일산대, 꽃동네대, 부산대, 청주대) | 202507_대학리스트_찐최종.md |
| Q8-3 | **2, 3, 4, 5번** | 숙박비 18만원/OmegaERP 9월/법인카드 800만원/인턴 8월5일 |

### 미해결 문항
| 문항 | 필요 정보 | 선택지 |
|------|-----------|--------|
| Q8-1 | AutoFlow 교육 장소 | 1층 대강당/3층 소강당/3층 대회의실/4층 소강당/4층 대회의실 |
| Q8-4 | 인수인계 문서 완성 | template.md 기반 |

### 음성 파일 정보
```
d:\repo\AI_TOP_100\source\q8\5_통화\5_통화\
├── 2025_04_30.m4a
├── 2025_05_20.m4a
├── 2025_05_28.m4a  (김하늘 생일 전날)
├── 2025_06_03.m4a
├── 2025_06_12.m4a
├── 2025_07_15.m4a  ★ AutoFlow 관련 가능성
└── 2025_07_18.m4a  ★ AutoFlow 관련 가능성
```
- ZIP 비밀번호: `0529` (김하늘 생일 5월 29일)
- 이미 추출 완료됨

### 찾아야 할 키워드
- AutoFlow, 교육, 대강당/소강당/대회의실, 1층/3층/4층, 7월 25일

### 다음 단계
1. [ ] ffmpeg 설치 (Windows: `choco install ffmpeg`)
2. [ ] Whisper로 7개 음성 파일 Transcript 추출
3. [ ] AutoFlow 교육 장소 확인
4. [ ] template.md 기반 인수인계 문서 작성

### Whisper 사용 코드
```bash
uv pip install openai-whisper

python -c "
import whisper
model = whisper.load_model('base')
result = model.transcribe('2025_07_15.m4a', language='ko')
print(result['text'])
"
```

---

## Q9. 스파이의 요리코드 (본선) - 0/5

**Source**: source/q9 (1.txt ~ 5.txt, cookingguide.png)
**문제**: 요리코드 인터프리터 구현 → 5개 문제 해결

### 요리코드 문법 요약
| 명령어 | 동작 |
|--------|------|
| 식기에 재료를 N번 넣는다 | 식기 += 재료값 × N |
| A의 내용물을 B로 옮긴다 | B += A, A = 0 |
| 식기를 N분간 가열한다 | 식기 × N |
| 식기를 N초간 가열한다 | 식기 // (60/N) |
| 식기를 식탁 위에 올려두었다 | print(식기) |
| 만약 A가 B보다 내용물이 많으면: ... 끝. | if A > B: ... |
| 레시피: ... 끝. / X번 만든다 | 함수 정의/호출 |

### 문항 목록
| 문항 | 내용 | 배점 |
|------|------|------|
| Q9-1 | 제육볶음 출력값 (객관식: 3,89,6 / 6,78,14 / 9,83,12 / 12,96,24) | 10점 |
| Q9-2 | 비밀재료 역추적 (은빛가루, 홍염장, 별사리 Kcal) | 10점 |
| Q9-3 | 행사용 사리곰탕 - 대규모 반복 | 15점 |
| Q9-4 | 긴 요리코드 실행 | 15점 |
| Q9-5 | 결행일 해독 (11/23~12/02 중 선택) | 20점 |

### 다음 단계
1. [ ] 요리코드 인터프리터 Python 구현
2. [ ] 1.txt 실행 → Q9-1 답 확인
3. [ ] 2.txt 역산 → Q9-2 비밀재료 복구
4. [ ] 3.txt ~ 5.txt 실행

---

## 우선순위 정리

### 1순위: 즉시 가능 (도구 준비됨)
- **Q9 요리코드** - 인터프리터 구현만 하면 됨

### 2순위: 추가 설정 필요
- **Q8 인수인계** - ffmpeg + Whisper 설치 → 음성 Transcript
- **Q6 입국 심사관** - OCR 도구 설정 → 이미지 PDF 텍스트 추출

### 3순위: 외부 리소스 필요
- **Q3 영상 팩트체크** - Ollama + VLM 설치 → 영상 분석
- **Q7 몽타주** - API 엔드포인트 + 이미지 생성 AI
- **Q5 PDF 추적** - 5번째 노래 추가 검색

---

## 파일 구조
```
d:\repo\AI_TOP_100\
├── question/               # 문제 정의 (1~9)
├── source/                 # 문제 데이터
│   ├── q1/ ~ q9/
├── TODO_COMPLETE.md        # 이 파일
└── .claude/plans/          # 작업 계획
```
