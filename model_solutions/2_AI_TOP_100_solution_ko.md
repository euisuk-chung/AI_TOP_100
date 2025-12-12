# 모범 답안: Q2. 배틀 게임 시뮬레이션

## 분석
이것은 머신러닝 분류 문제입니다.
**목표**: 유닛 배치 좌표를 기반으로 게임 승리(블루/레드)를 예측합니다.
**데이터**: `train_battles.json` (없음), `test_battles.json` (없음).

## 풀이 접근법

### 1. 데이터 로딩 및 피처 엔지니어링
JSON 데이터를 ML에 적합한 형식(예: Pandas DataFrame)으로 변환해야 합니다.
추출할 주요 피처:
-   **유닛 수**: 팀별 각 유닛 타입(aleo, bras, cbene, dgreg, eyanoo)의 수.
-   **무게 중심**: 각 팀의 평균 (x, y) 좌표.
-   **분산/퍼짐도**: 유닛들이 얼마나 퍼져 있는지 (x와 y의 표준편차).
-   **전방/후방 수**: "전방" vs "후방"에 있는 유닛 수 (수직 이등분선으로 정의).

### 2. 모델 선택
입력 피처가 테이블 형식이고 데이터셋 크기가 적당할 것으로 예상되므로, **Random Forest** 또는 **XGBoost**가 좋은 후보입니다.

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
    # 예시: 'blue' 팀의 유닛 수 추출
    features = {}
    blue_units = battle['blue_team']
    red_units = battle['red_team']

    # 타입별 유닛 수 계산
    for u_type in ['aleo', 'bras', 'cbene', 'dgreg', 'eyanoo']:
        features[f'blue_{u_type}'] = sum(1 for u in blue_units if u['type'] == u_type)
        features[f'red_{u_type}'] = sum(1 for u in red_units if u['type'] == u_type)

    # 중심 계산
    blue_x = np.mean([u['x'] for u in blue_units])
    blue_y = np.mean([u['y'] for u in blue_units])
    red_x = np.mean([u['x'] for u in red_units])
    red_y = np.mean([u['y'] for u in red_units])

    features['blue_x'] = blue_x
    features['blue_y'] = blue_y
    features['red_x'] = red_x
    features['red_y'] = red_y

    # ... 추가 피처 (전방/후방, 거리) 추가 ...

    return features

X = [extract_features(b) for b in train_data]
y = [1 if b['winner'] == 'blue' else 0 for b in train_data] # 블루 1, 레드 0

# 3. 모델 학습
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X, y)

# 4. 예측
X_test = [extract_features(b) for b in test_data]
predictions = clf.predict(X_test)

# 5. 출력 형식 맞추기
results = []
for i, pred in enumerate(predictions):
    winner = "blue" if pred == 1 else "red"
    results.append({"id": test_data[i]['id'], "winner": winner})

print(json.dumps(results, indent=2))
```

## 세부 질문 답변 (가설)

-   **Q1 (1v1 최강)**: `len(blue) == 1`이고 `len(red) == 1`인 배틀 부분집합을 분석합니다. 각 타입별 승률을 계산합니다.
-   **Q2 (배치 효과)**: 유닛 타입이 "전방"에 있을 때와 "후방"에 있을 때의 승률을 비교합니다.
-   **Q3 (진형)**: x-분산이 높은 팀과 y-분산이 높은 팀의 승률을 비교합니다.
-   **Q4 (상성)**: 1v1 시나리오에서 유닛 타입 간 승률 매트릭스를 구성합니다.
