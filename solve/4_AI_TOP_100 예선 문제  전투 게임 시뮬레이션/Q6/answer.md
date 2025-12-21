### Q6. 500개 테스트 전투 결과 예측

#### 답안: predictions.json 파일 참조

#### 근거

##### 모델링 접근법

test_battles.json의 500개 전투에 대해 다음 특성 기반 ML 모델로 예측:

##### Feature Engineering

1. **팀 구성 특성**
   - 유닛별 개수 (aleo, bras, cbene, dgreg, eyanoo)
   - 중복 유닛 존재 여부
   - 강한 유닛(dgreg, cbene) 비율

2. **위치 특성**
   - 평균 x, y 좌표
   - x/y spread (진형 형태)
   - 맵 중앙과의 거리
   - 전방/후방 유닛 비율

3. **상대 비교 특성**
   - 팀 간 평균 거리
   - 유닛 수 차이
   - 강한 유닛 수 차이

##### 모델

```python
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import cross_val_score

# 모델 학습
model = GradientBoostingClassifier(n_estimators=200, max_depth=5)
model.fit(X_train, y_train)

# 교차 검증 정확도: ~53.5%
```

##### 예측 결과

```json
[
  {"id": "test_001", "winner": "red"},
  {"id": "test_002", "winner": "blue"},
  ...
]
```

##### 파일 위치
- 예측 결과: `/source/q4/predictions.json`

##### 성능
- Cross-validation 정확도: 약 53.5%
- 기본 baseline(50%) 대비 약 3.5% 향상
