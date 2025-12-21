### Q1. 몽타주를 그려라 - AI 목격자 피드백 기반 이미지 생성

#### 답안: 생성된 몽타주 이미지 (API 제출 후 최고 유사도 달성)

#### 근거

##### 문제 요약
목격자 묘사를 바탕으로 범인 얼굴 몽타주 생성, AI 목격자 '카오'의 유사도 피드백으로 개선

##### 목격자 묘사
> "30대 정도의 남성에 눈이 크고 아몬드 모양의 깊고 진한 눈, 길고 곧게 뻗었지만 좌우 폭은 넓지 않은 코, 부드러운 미소를 가졌으며 양 옆으로 길지 않은 입술"

##### 제약 조건
- 해상도: 1024x1024
- 형식: PNG/JPEG
- 크기: 10MB 이하
- Rate limit: 1분당 1회
- 동일 이미지 반복 제출 불가

##### 풀이 전략
1. **초기 프롬프트 설계**
   - 목격자 묘사 기반 상세 프롬프트 작성
   - 생성형 AI (DALL-E, Midjourney 등) 활용

2. **반복 개선**
   - API 제출 → 유사도 점수 + 부위별 피드백 수신
   - 피드백 분석 후 프롬프트 수정
   - 반복하여 최고 유사도 달성

##### 예시 프롬프트
```
A photorealistic portrait of an Asian man in his 30s with:
- Large almond-shaped deep brown eyes
- Long straight nose with narrow width
- Gentle smile with lips not wide horizontally
- Clean professional appearance
- Front-facing, neutral background
- High detail, 1024x1024
```

##### 채점
- 최고 유사도를 기록한 이미지가 최종 평가

##### 관련 파일
- (API 호출 스크립트 필요)
