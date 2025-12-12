# 모범 답안: Q4. 전투 없이 예측하는 시뮬레이션의 힘

## 출제 의도

### 문제 패턴

**P4. 최적화/의사결정 (Decision)** - 제약 조건 하에서 목표를 최대화하는 최적의 의사결정을 내리는 시뮬레이션

### 핵심 측정 역량

1. **데이터 분석 능력**: 전투 데이터에서 의미 있는 패턴과 피처를 추출
2. **ML 모델링 역량**: 분류 문제에 적합한 모델 선택 및 학습
3. **명시적 검증 유도**: 참가자가 직접 검증 데이터셋을 구성하여 모델 성능 확인

### 왜 '딸깍'으로 풀리지 않는가?

- 단순히 "이 데이터로 승자를 예측해줘"라고 요청하면 **정확도가 낮음**
- 유닛의 **상성 관계**, **배치 위치**, **진형** 등 복합적인 요소를 고려해야 함
- **피처 엔지니어링**이 성능에 큰 영향을 미침 - 사람의 도메인 지식 필요

### 난이도 구조

- **Q1 (Easy)**: 1v1 최강 유닛 찾기 - 단순 통계 분석
- **Q2 (Medium)**: 배치 효과 분석 - 전방/후방 개념 이해 필요
- **Q3 (Medium)**: 진형 분석 - 공간적 분포 이해 필요
- **Q4 (Hard)**: 상성표 작성 - 복합 분석 및 시각화

---

## 권장 접근법

### 1단계: 사람의 분석

- 데이터 구조 파악: 각 전투의 팀 구성, 유닛 위치, 승패 정보
- 도메인 지식 적용: 게임에서 일반적으로 중요한 요소들 (유닛 수, 위치, 타입)

### 2단계: AI와의 협업

```text
프롬프트 예시:
"이 전투 데이터를 분석해줘. 각 전투에서 블루팀과 레드팀의
유닛 배치 정보가 있고, 승자가 기록되어 있어.

1. 먼저 데이터 구조를 파악하고
2. 승패에 영향을 미칠 수 있는 피처들을 추출해줘
3. 피처로는 유닛 수, 유닛 타입별 수, 무게중심, 분산 등을 고려해줘"
```

### 3단계: 사람의 검증

1. 학습 데이터를 train/validation으로 분리하여 모델 성능 검증
2. 예측 결과의 패턴 분석 - 어떤 경우에 틀리는지 확인
3. 피처 중요도 분석 - 모델이 어떤 요소를 중요하게 보는지 확인

---

## 풀이

### 1. 데이터 로딩 및 피처 엔지니어링

JSON 데이터를 ML에 적합한 형식으로 변환합니다.

추출할 주요 피처:

- **유닛 수**: 팀별 각 유닛 타입(aleo, bras, cbene, dgreg, eyanoo)의 수
- **무게 중심**: 각 팀의 평균 (x, y) 좌표
- **분산/퍼짐도**: 유닛들이 얼마나 퍼져 있는지 (x와 y의 표준편차)
- **전방/후방 수**: "전방" vs "후방"에 있는 유닛 수

### 2. 모델 선택

입력 피처가 테이블 형식이고 데이터셋 크기가 적당하므로, **Random Forest** 또는 **XGBoost**가 좋은 후보입니다.

### 3. Python 풀이 스크립트

```python
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# 1. 데이터 로드
def load_data(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

train_data = load_data('train_battles.json')
test_data = load_data('test_battles.json')

# 2. 피처 엔지니어링
def extract_features(battle):
    features = {}
    blue_units = battle['blue_team']
    red_units = battle['red_team']

    # 타입별 유닛 수 계산
    for u_type in ['aleo', 'bras', 'cbene', 'dgreg', 'eyanoo']:
        features[f'blue_{u_type}'] = sum(1 for u in blue_units if u['type'] == u_type)
        features[f'red_{u_type}'] = sum(1 for u in red_units if u['type'] == u_type)

    # 중심 계산
    if blue_units:
        features['blue_x'] = np.mean([u['x'] for u in blue_units])
        features['blue_y'] = np.mean([u['y'] for u in blue_units])
    if red_units:
        features['red_x'] = np.mean([u['x'] for u in red_units])
        features['red_y'] = np.mean([u['y'] for u in red_units])

    return features

X = [extract_features(b) for b in train_data]
y = [1 if b['winner'] == 'blue' else 0 for b in train_data]

# 3. 모델 학습 및 검증
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(pd.DataFrame(X_train), y_train)

# 검증
val_pred = clf.predict(pd.DataFrame(X_val))
print(f"Validation Accuracy: {accuracy_score(y_val, val_pred)}")

# 4. 예측
X_test = [extract_features(b) for b in test_data]
predictions = clf.predict(pd.DataFrame(X_test))

# 5. 결과 출력
results = []
for i, pred in enumerate(predictions):
    winner = "blue" if pred == 1 else "red"
    results.append({"id": test_data[i]['id'], "winner": winner})

print(json.dumps(results, indent=2))
```

---

## 세부 질문 답변

### Q1 (1v1 최강)

`len(blue) == 1`이고 `len(red) == 1`인 배틀 부분집합을 필터링하여 각 타입별 승률을 계산합니다.

### Q2 (배치 효과)

유닛 타입이 "전방"에 있을 때와 "후방"에 있을 때의 승률을 비교합니다. 전방/후방은 맵의 중앙선 또는 상대팀 방향을 기준으로 정의합니다.

### Q3 (진형)

x-분산이 높은 팀(가로로 펼친 진형)과 y-분산이 높은 팀(세로로 펼친 진형)의 승률을 비교합니다.

### Q4 (상성)

1v1 시나리오에서 유닛 타입 간 승률 매트릭스를 구성합니다. 행은 블루팀 유닛, 열은 레드팀 유닛으로 하여 각 조합의 승률을 계산합니다.

---

## 핵심 교훈

> "ML 문제에서 AI는 강력한 도구이지만, **어떤 피처를 추출할지**, **어떻게 검증할지**는 사람의 도메인 지식이 결정한다."

이 문제는 데이터 분석과 ML 모델링에서 **사람의 분석적 사고**와 **AI의 계산 능력**이 어떻게 협업해야 하는지를 보여줍니다.
