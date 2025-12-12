# 모범 답안: Q7. 몽타주 그리기

## 분석
**목표**: 텍스트 설명을 기반으로 이미지를 생성합니다.
**도구**: 생성형 AI (DALL-E, Midjourney, Stable Diffusion).

## 프롬프트 엔지니어링
핵심은 목격자 증언을 구조화된 프롬프트로 변환하는 것입니다.

**목격자 증언**:
"용의자는 30대 남성입니다. 짧은 검은 머리와 갈색 눈을 가지고 있습니다. 둥근 얼굴형에 작은 코를 가지고 있습니다. 두꺼운 눈썹과 얇은 입술을 가지고 있습니다. 검은색 재킷과 청바지를 입고 있었습니다."

**최적화된 프롬프트**:
> A realistic police sketch style portrait of a suspect. Male, 30s, short black hair, brown eyes, round face shape, small nose, thick eyebrows, thin lips. Wearing a black jacket. Neutral expression, facing forward. High quality, detailed pencil sketch texture.

(한국어 버전):
> 용의자의 사실적인 경찰 몽타주 스타일 초상화. 남성, 30대, 짧은 검은 머리, 갈색 눈, 둥근 얼굴형, 작은 코, 두꺼운 눈썹, 얇은 입술. 검은색 재킷 착용. 무표정, 정면을 향함. 고품질, 상세한 연필 스케치 질감.

## 풀이 단계
1.  AI 이미지 생성기를 엽니다 (예: ChatGPT, Midjourney).
2.  최적화된 프롬프트를 입력합니다.
3.  모든 특징과 일치하는 최상의 결과를 선택합니다.
4.  `montage.png`로 저장합니다.

*(저는 텍스트 기반 AI이므로 여기서 실제 이미지 파일을 생성할 수 없지만, 위의 프롬프트가 이미지를 생성하기 위한 "풀이"입니다.)*
