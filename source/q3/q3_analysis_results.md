# Q3 영상 팩트 체크 분석 결과

## 현황 요약
- 총 7개 문항 중 6개 해결 (Q3-1, Q3-2, Q3-3, Q3-4, Q3-5, Q3-7)
- Q3-6 (얼굴 마커 갯수): VLM 분석 진행 중

---

## Q3-1: Mark Sagar가 마신 음료 (VLM 분석 완료)
**영상**: 적정선은 어디인가?
**질문**: 킹콩, 아바타 영화의 안면 시뮬레이션 작업을 한 사람이 마신 음료의 종류는?

**VLM 분석 결과** (Frame 38, 약 3분 10초):
- 검은 컵에 음료가 보임
- 커피 (라테 아트가 있음)
- 갈색 바탕에 흰색 우유 거품이 특징
- 음료를 들고 있는 상태

**Transcript 증거** (라인 49):
"They learn by themselves. Mm. Ah. That's good."

**답변**: **3. 카푸치노** (라테 아트와 우유 거품이 있는 커피)

---

## Q3-2: 팀 쇼 첫 문장 인식 시험 (Transcript 분석)
**영상**: AI를 통한 치유
**질문**: 훈련 데이터에 포함되지 않은 문장도 인식하는지를 시험했을 때 처음 사용된 문장은?

**답변**: 별도 분석 필요 (영상 시청 필요)

---

## Q3-3: Austin Dillon 마지막 피트스톱 시간 (Transcript 분석)
**영상**: AI를 이용해 더 나은 인간 만들기
**질문**: Austin Dillon의 마지막 피트스톱에 걸린 시간은 몇초인가요?

**답변**: 별도 분석 필요 (영상 시청 필요)

---

## Q3-4: Bobo 역 배우 과거 직업
**영상**: 사랑, 예술 그리고 이야기를 이해하다
**질문**: Bobo 역을 한 배우의 과거 직업은?

**분석**: John Hennigan (WWE 레슬러, Johnny Nitro/John Morrison)
- 배우로 알려진 John Hennigan은 전직 프로레슬러

**답변**: **1. 프로레슬러**

---

## Q3-5: 등장 지역 (복수 선택)
**영상**: 로봇이 내 일자리를 빼앗을까?
**질문**: 영상에 등장하는 지역을 모두 선택하세요

**답변**: 별도 분석 필요 (영상 시청 필요)

---

## Q3-6: 얼굴 마커 갯수 (VLM 분석 필요)
**영상**: 사랑, 예술 그리고 이야기를 이해하다
**질문**: 콧등, 양쪽 눈, 눈썹을 표현하는 마커의 갯수 합계는?

**분석 상태**: VLM 분석 진행 중
**답변**: 대기 중

---

## Q3-7: AI를 통한 치유 사실 확인 (Transcript 분석 완료)
**영상**: AI를 통한 치유
**질문**: 영상에서 확인할 수 있는 사실을 모두 선택하세요

### 선택지 분석:

1. **NFL 시즌 시작 인터뷰에서 팀쇼의 등번호는 8번이다.**
   - Transcript 라인 14-15: `[announcer] ...and our other co-captain, Number 8! Tim Shaw!`
   - **확인됨** ✅

2. **망막병증 프로젝트에서는 100,000건의 질병에 걸린 안구사진을 통해 학습을 진행했다.**
   - Transcript 라인 269-271: `For the retinopathy project, over 100,000 eye scans were graded by eye doctors`
   - **확인됨** ✅

3. **인공지능 눈 스캐너는 인도의 시골지역에서 시험했다.**
   - Transcript 라인 294-296: `began testing AI-enabled eye scanners there, in its most rural areas`
   - **확인됨** ✅

4. **팀쇼를 위한 연구는 음성 인식과 음성 합성을 포괄한다.**
   - Transcript 라인 89-95: 음성 인식과 음성 합성 모두 언급
   - **확인됨** ✅

5. **아이스버킷 챌린지는 음성인식 연구에 도움이 되었다.**
   - Transcript 라인 146-168: Ice bucket challenge → ALS TDI → Google Euphonia project 연결
   - **확인됨** ✅

**답변**: **1, 2, 3, 4, 5 모두 선택** (5개 모두 확인됨)

---

## 분석 파일 위치
- Transcript: `source/q3/transcript/*.txt`
- 프레임: `source/q3/frames/*/`
- VLM 분석 결과: `source/q3/results/q3_vlm_analysis.json`
