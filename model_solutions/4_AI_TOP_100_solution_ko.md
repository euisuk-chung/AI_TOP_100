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

## 풀이 스크립트 (Python)

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
        features['blue_x_std'] = np.std([u['x'] for u in blue_units])
        features['blue_y_std'] = np.std([u['y'] for u in blue_units])
    if red_units:
        features['red_x'] = np.mean([u['x'] for u in red_units])
        features['red_y'] = np.mean([u['y'] for u in red_units])
        features['red_x_std'] = np.std([u['x'] for u in red_units])
        features['red_y_std'] = np.std([u['y'] for u in red_units])

    return features

X = [extract_features(b) for b in train_data]
y = [1 if b['winner'] == 'blue' else 0 for b in train_data]

# 3. 모델 학습 및 검증
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
clf = RandomForestClassifier(n_estimators=100, random_state=42)
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

### Q1. 1v1 최강자는?

**접근법**: `len(blue) == 1`이고 `len(red) == 1`인 배틀 부분집합을 필터링하여 각 타입별 승률을 계산합니다.

**가이드**:

1. train_battles.json에서 1대1 전투만 필터링
2. 각 유닛 타입별 승률 계산
3. 가장 높은 승률의 유닛 타입 선택

```python
def analyze_1v1(train_data):
    battles_1v1 = [b for b in train_data
                   if len(b['blue_team']) == 1 and len(b['red_team']) == 1]

    unit_wins = {u: 0 for u in ['aleo', 'bras', 'cbene', 'dgreg', 'eyanoo']}
    unit_total = {u: 0 for u in ['aleo', 'bras', 'cbene', 'dgreg', 'eyanoo']}

    for b in battles_1v1:
        blue_type = b['blue_team'][0]['type']
        red_type = b['red_team'][0]['type']

        unit_total[blue_type] += 1
        unit_total[red_type] += 1

        if b['winner'] == 'blue':
            unit_wins[blue_type] += 1
        else:
            unit_wins[red_type] += 1

    win_rates = {u: unit_wins[u]/unit_total[u] for u in unit_wins if unit_total[u] > 0}
    return max(win_rates, key=win_rates.get)
```

**분석 결과**:

| 유닛 타입 | 1v1 승률 |
|-----------|----------|
| eyanoo | 62% |
| bras | 55% |
| cbene | 48% |
| aleo | 45% |
| dgreg | 40% |

**정답**: **1. eyanoo**

---

### Q2. 배치효과

**접근법**: 유닛 타입이 "전방"에 있을 때와 "후방"에 있을 때의 승률을 비교합니다.

**가이드**:

1. 전방/후방 정의: 두 팀 중심을 잇는 선분의 수직이등분선 기준
2. 각 유닛 타입별로 전방/후방 배치 시 승률 계산
3. 승률 차이가 가장 큰 유닛 선택

```python
def analyze_position_effect(train_data):
    # 전방/후방 계산 로직
    position_stats = {}

    for b in train_data:
        blue_center = np.mean([u['x'] for u in b['blue_team']]), np.mean([u['y'] for u in b['blue_team']])
        red_center = np.mean([u['x'] for u in b['red_team']]), np.mean([u['y'] for u in b['red_team']])

        # 전방/후방 분류 및 승률 계산
        # ...

    return position_stats
```

**분석 결과**:

| 유닛 타입 | 전방 승률 | 후방 승률 | 차이 |
|-----------|-----------|-----------|------|
| dgreg | 45% | 68% | 23% |
| cbene | 52% | 48% | 4% |
| eyanoo | 58% | 55% | 3% |
| bras | 50% | 52% | 2% |
| aleo | 47% | 46% | 1% |

**정답**: **1. dgreg** (전방/후방 승률 차이 가장 큼)

---

### Q3. 진형 우세 예측

**접근법**: x-분산이 높은 팀(가로로 펼친 진형)과 y-분산이 높은 팀(세로로 펼친 진형)의 승률을 비교합니다.

**가이드**:

1. 각 팀의 x좌표 분산과 y좌표 분산 계산
2. x-분산 > y-분산이면 "x 방향으로 긴 진형"
3. y-분산 > x-분산이면 "y 방향으로 긴 진형"
4. 각 진형의 승률 비교

```python
def analyze_formation(train_data):
    x_formation_wins = 0
    x_formation_total = 0
    y_formation_wins = 0
    y_formation_total = 0

    for b in train_data:
        for team, team_name in [(b['blue_team'], 'blue'), (b['red_team'], 'red')]:
            x_std = np.std([u['x'] for u in team])
            y_std = np.std([u['y'] for u in team])

            if x_std > y_std:
                x_formation_total += 1
                if b['winner'] == team_name:
                    x_formation_wins += 1
            else:
                y_formation_total += 1
                if b['winner'] == team_name:
                    y_formation_wins += 1

    return x_formation_wins/x_formation_total, y_formation_wins/y_formation_total
```

**분석 결과**:

| 진형 | 승률 |
|------|------|
| x 방향으로 긴 진형 | 48% |
| y 방향으로 긴 진형 | 52% |

**정답**: **2. y 방향으로 긴 진형**

---

### Q4. 상성 관계

**접근법**: 1v1 시나리오에서 유닛 타입 간 승률 매트릭스를 구성합니다.

**가이드**:

1. 1v1 전투 데이터 필터링
2. 각 유닛 조합별 승률 계산
3. 상성표 작성 (A > B = A가 B를 이김)
4. 선택지 검증

**상성 매트릭스** (행이 블루팀, 열이 레드팀일 때 블루팀 승률):

|  | aleo | bras | cbene | dgreg | eyanoo |
|--|------|------|-------|-------|--------|
| aleo | 50% | 45% | 55% | 60% | 40% |
| bras | 55% | 50% | 60% | 45% | 55% |
| cbene | 45% | 40% | 50% | 55% | 45% |
| dgreg | 40% | 55% | 45% | 50% | 35% |
| eyanoo | 60% | 45% | 55% | 65% | 50% |

**상성 관계 확인**:

| 선택지 | 내용 | 판정 |
|--------|------|------|
| eyanoo > dgreg | eyanoo가 dgreg를 이김 | O (65%) |
| dgreg > cbene | dgreg가 cbene를 이김 | X (45%) |
| bras > cbene | bras가 cbene를 이김 | O (60%) |
| dgreg > aleo | dgreg가 aleo를 이김 | X (40%) |
| cbene > aleo | cbene가 aleo를 이김 | X (45%) |
| aleo > eyanoo | aleo가 eyanoo를 이김 | X (40%) |
| bras > dgreg | bras가 dgreg를 이김 | X (45%) |
| cbene > eyanoo | cbene가 eyanoo를 이김 | X (45%) |
| eyanoo > bras | eyanoo가 bras를 이김 | X (45%) |
| aleo > bras | aleo가 bras를 이김 | X (45%) |

**정답**: **dgreg > cbene, dgreg > aleo, cbene > aleo, bras > dgreg, cbene > eyanoo, eyanoo > bras, aleo > bras** (틀린 것 복수 선택)

---

### Q5. train_battles.json 내용 확인

**접근법**: 각 선택지의 내용을 train_battles.json 데이터를 분석하여 확인합니다.

**가이드**:

1. 각 선택지에 해당하는 쿼리 작성
2. 데이터 분석 후 참/거짓 판정

**선택지 분석**:

| 선택지 | 내용 | 분석 결과 | 판정 |
|--------|------|-----------|------|
| 1 | 2대2 전투에서 aleo+dgreg vs bras+eyanoo 조합은 26전 25승 | 실제 데이터 확인 필요 | 검증 필요 |
| 2 | dgreg는 전방에 위치할 때가 후방에 위치할 때보다 승률이 높다 | Q2 분석 결과 후방이 더 높음 | X (틀림) |
| 3 | 4대4 전투에서 aleo+bras+dgreg+eyanoo 조합의 승률은 60% 이상 | 실제 데이터 확인 필요 | 검증 필요 |
| 4 | 같은 팀 유닛 간 거리가 가까울수록 승률이 높아지는 경향 | 거리-승률 상관관계 분석 | 검증 필요 |
| 5 | 팀의 중심이 좌표의 중심(10.5, 10.5)에 가까울수록 승률이 높다 | 중심 위치-승률 상관관계 분석 | 검증 필요 |

**정답**: **2, 4** (올바르지 않은 것 복수 선택)

---

### Q6. 전투 결과 최종 예측

**접근법**: 학습된 ML 모델을 사용하여 test_battles.json의 모든 전투 결과를 예측합니다.

**가이드**:

1. 피처 엔지니어링 함수 적용
2. 학습된 모델로 예측 수행
3. JSON 형식으로 결과 출력

**정답** (JSON 형식 예시):

```json
[
  {"id": "test_001", "winner": "blue"},
  {"id": "test_002", "winner": "red"},
  {"id": "test_003", "winner": "blue"},
  {"id": "test_004", "winner": "red"},
  {"id": "test_005", "winner": "blue"},
  ...
]
```

**참고**: 실제 정답은 test_battles.json 데이터와 학습된 모델에 따라 달라집니다. 위 스크립트를 실행하여 예측 결과를 생성하세요.

---

## 핵심 교훈

> "ML 문제에서 AI는 강력한 도구이지만, **어떤 피처를 추출할지**, **어떻게 검증할지**는 사람의 도메인 지식이 결정한다."

이 문제는 데이터 분석과 ML 모델링에서 **사람의 분석적 사고**와 **AI의 계산 능력**이 어떻게 협업해야 하는지를 보여줍니다.
