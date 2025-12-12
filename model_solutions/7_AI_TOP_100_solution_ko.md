# 모범 답안: Q7. 몽타주를 그려라

## 출제 의도

### 문제 패턴

**P2. 구현 및 자동화 (Action)** - 정의된 문제를 해결하기 위해 AI 솔루션을 실제 작동하는 코드나 워크플로로 구현

### 핵심 측정 역량

1. **프롬프트 엔지니어링**: 텍스트 설명을 효과적인 이미지 생성 프롬프트로 변환
2. **생성 AI 활용 능력**: DALL-E, Midjourney, Stable Diffusion 등 적절한 도구 선택
3. **반복적 개선**: 생성 결과를 평가하고 프롬프트를 수정하여 품질 향상
4. **암묵적 검증 유도**: 목격자 증언의 모든 특징이 반영되었는지 확인

### 왜 '딸깍'으로 풀리지 않는가?

- "이 사람 그려줘"라고 단순히 요청하면 **원하는 스타일이 아닐 수 있음**
- 목격자 증언의 모든 특징(얼굴형, 눈썹, 입술 등)이 **정확히 반영되지 않을 수 있음**
- 경찰 몽타주 스타일을 구현하려면 **특정 프롬프트 기법** 필요
- 여러 번 생성하고 **가장 적합한 결과를 선택**하는 과정 필요

### 난이도 구조

- **Q1 (Medium)**: 기본 몽타주 생성 - 프롬프트 구성 능력
- **추가 도전**: 여러 특징을 정확히 반영 - 반복적 개선 필요

---

## 권장 접근법

### 1단계: 사람의 분석

- 목격자 증언에서 핵심 특징 추출 및 구조화
- 경찰 몽타주 스타일의 특성 파악 (흑백, 연필 스케치, 정면 얼굴)
- 생성 AI 도구의 강점과 제약 이해

### 2단계: AI와의 협업

```text
프롬프트 예시:
"목격자 증언을 바탕으로 경찰 몽타주용 이미지 생성 프롬프트를 만들어줘.

증언 내용:
'용의자는 30대 남성입니다. 짧은 검은 머리와 갈색 눈을 가지고 있습니다.
둥근 얼굴형에 작은 코를 가지고 있습니다. 두꺼운 눈썹과 얇은 입술을
가지고 있습니다. 검은색 재킷과 청바지를 입고 있었습니다.'

프롬프트 요구사항:
1. 영어로 작성 (대부분의 생성 AI가 영어에 최적화)
2. 경찰 몽타주/스케치 스타일 명시
3. 모든 얼굴 특징 포함
4. 정면 얼굴, 중립적 표정 지정"
```

### 3단계: 사람의 검증

1. 생성된 이미지와 **목격자 증언 대조** - 모든 특징 반영 확인
2. 스타일이 **경찰 몽타주에 적합한지** 평가
3. 부족한 부분은 **프롬프트 수정 후 재생성**
4. 여러 결과 중 **가장 적합한 이미지 선택**

---

## 프롬프트 엔지니어링

### 목격자 증언

"용의자는 30대 남성입니다. 짧은 검은 머리와 갈색 눈을 가지고 있습니다. 둥근 얼굴형에 작은 코를 가지고 있습니다. 두꺼운 눈썹과 얇은 입술을 가지고 있습니다. 검은색 재킷과 청바지를 입고 있었습니다."

### 특징 분해

| 카테고리 | 특징 | 영어 표현 |
|----------|------|-----------|
| 성별/나이 | 30대 남성 | Male, 30s |
| 머리 | 짧은 검은 머리 | Short black hair |
| 눈 | 갈색 눈 | Brown eyes |
| 얼굴형 | 둥근 얼굴 | Round face shape |
| 코 | 작은 코 | Small nose |
| 눈썹 | 두꺼운 눈썹 | Thick eyebrows |
| 입술 | 얇은 입술 | Thin lips |
| 의상 | 검은색 재킷 | Black jacket |

### 최적화된 프롬프트 (영어)

```
A realistic police sketch style portrait of a suspect.
Male, 30s, short black hair, brown eyes, round face shape,
small nose, thick eyebrows, thin lips.
Wearing a black jacket.
Neutral expression, facing forward.
High quality, detailed pencil sketch texture,
black and white forensic composite style.
```

### 최적화된 프롬프트 (한국어 버전)

```
용의자의 사실적인 경찰 몽타주 스타일 초상화.
남성, 30대, 짧은 검은 머리, 갈색 눈, 둥근 얼굴형,
작은 코, 두꺼운 눈썹, 얇은 입술.
검은색 재킷 착용.
무표정, 정면을 향함.
고품질, 상세한 연필 스케치 질감,
흑백 법의학 합성 스타일.
```

---

---

### Q1. 몽타주 이미지 제출 (최고 유사도 달성)

**접근법**: 목격자 증언을 분석하여 생성형 AI에 최적화된 프롬프트를 설계하고, API 피드백을 기반으로 반복적으로 개선하여 최고 유사도를 달성합니다.

**가이드**:

1. **목격자 증언 분석 및 특징 추출**:

| 카테고리 | 원문 | 영어 프롬프트 |
|----------|------|---------------|
| 성별/나이 | 30대 정도의 남성 | Male in his 30s |
| 눈 | 눈이 크고 아몬드 모양의 깊고 진한 눈 | Large almond-shaped deep dark eyes |
| 코 | 길고 곧게 뻗었지만 좌우 폭은 넓지 않은 코 | Long straight nose with narrow width |
| 입 | 부드러운 미소를 가졌으며 양 옆으로 길지 않은 입술 | Soft smile with short lips |

2. **최적화된 프롬프트 작성**:

```
A realistic police forensic sketch portrait.
Male suspect in his 30s.
Large almond-shaped deep dark eyes.
Long straight nose with narrow width.
Soft gentle smile with short lips that don't extend wide.
Neutral expression, front-facing view.
High quality detailed pencil sketch, black and white,
forensic composite style, professional police sketch.
```

3. **API 제출 및 피드백 분석**:
   - 1024x1024 해상도 PNG/JPEG로 저장
   - API에 제출하여 유사도 점수와 부위별 피드백 확인
   - 피드백에 따라 프롬프트 수정 (예: "눈을 더 크게", "코를 더 좁게")

4. **반복 개선**:
   - 부족한 특징 강조: `prominently large almond eyes`, `distinctly narrow nose bridge`
   - 스타일 조정: `graphite pencil texture`, `high contrast sketch`
   - rate limit (1분당 1회) 고려하여 신중하게 제출

**프롬프트 개선 팁**:

```
-- 눈이 부족할 때 --
"with strikingly large, deep-set almond-shaped dark brown eyes"

-- 코가 부족할 때 --
"elongated straight nose with notably narrow bridge"

-- 입이 부족할 때 --
"gentle subtle smile with compact lips"
```

**정답**: AI 이미지 생성 도구(DALL-E, Midjourney, Stable Diffusion 등)를 활용하여 목격자 증언의 모든 특징을 반영한 몽타주를 생성하고, API 피드백을 기반으로 반복 개선하여 최고 유사도를 기록한 이미지를 `montage.png`로 제출합니다.

---

## 풀이 단계

1. **AI 이미지 생성기 선택**
   - ChatGPT (DALL-E 3) - 가장 접근성 좋음
   - Midjourney - 고품질이지만 Discord 필요
   - Stable Diffusion - 로컬 설치 가능, 세밀한 조정 가능

2. **프롬프트 입력 및 생성**
   - 최적화된 프롬프트 입력
   - 여러 버전 생성 (보통 4개)

3. **결과 평가**
   - 각 특징이 정확히 반영되었는지 체크리스트로 확인
   - 경찰 몽타주 스타일에 적합한지 평가

4. **반복 개선 (필요시)**
   - 부족한 특징 강조: "더 두꺼운 눈썹", "더 둥근 얼굴"
   - 스타일 조정: "더 스케치 느낌", "흑백으로"

5. **최종 선택 및 저장**
   - 가장 적합한 이미지를 `montage.png`로 저장

---

## 프롬프트 개선 팁

### 특징이 잘 반영되지 않을 때

```
-- 눈썹을 더 강조하고 싶을 때 --
"with prominently thick, dark eyebrows"

-- 얼굴형을 더 명확히 하고 싶을 때 --
"distinctly round face with soft jaw line"

-- 스케치 스타일을 더 강조하고 싶을 때 --
"graphite pencil forensic sketch, high contrast,
detailed cross-hatching technique"
```

### 부정 프롬프트 (Stable Diffusion용)

```
Negative prompt:
photorealistic, color, smiling, 3d render,
anime style, cartoon, blurry, low quality
```

---

## 핵심 교훈

> "이미지 생성 AI는 **프롬프트의 품질**에 따라 결과가 크게 달라진다. **사람이 특징을 구조화**하고 **적절한 프롬프트로 변환**하는 능력이 핵심이다."

이 문제는 생성 AI 활용에서 **프롬프트 엔지니어링의 중요성**을 보여줍니다. 단순히 "그려줘"가 아니라 **구체적이고 구조화된 지시**가 원하는 결과를 얻는 열쇠입니다.
