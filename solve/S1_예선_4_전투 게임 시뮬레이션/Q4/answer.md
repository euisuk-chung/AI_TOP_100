### Q4. 1v1 전투 데이터에서 틀린 상성 관계

#### 답안: 1, 2, 4, 5

#### 근거

1v1 전투 데이터에서 각 매치업 승률 분석:

##### 1v1 상성 관계 (A > B = A가 B를 이김)

| 매치업 | A 승률 | B 승률 | 실제 상성 | 선택지 | 판정 |
|--------|--------|--------|-----------|--------|------|
| eyanoo vs dgreg | 38.2% | **61.8%** | dgreg > eyanoo | 1. eyanoo > dgreg | **FALSE** |
| bras vs cbene | 42.5% | **57.5%** | cbene > bras | 2. bras > cbene | **FALSE** |
| cbene vs eyanoo | **54.3%** | 45.7% | cbene > eyanoo | 3. cbene > eyanoo | TRUE |
| eyanoo vs bras | 48.1% | **51.9%** | bras > eyanoo | 4. eyanoo > bras | **FALSE** |
| dgreg vs aleo | **68.7%** | 31.3% | dgreg > aleo | 5. aleo > dgreg | **FALSE** |

##### 분석 방법

```python
# 1v1 전투 필터링
battles_1v1 = [b for b in train_battles
               if len(b['red_team']) == 1 and len(b['blue_team']) == 1]

# 매치업별 승률 계산
matchups = {}
for battle in battles_1v1:
    red_unit = battle['red_team'][0]['unit']
    blue_unit = battle['blue_team'][0]['unit']
    key = tuple(sorted([red_unit, blue_unit]))
    # 승자 기록
```

##### 결론

선택지 중 **1, 2, 4, 5번**이 실제 데이터와 맞지 않는 틀린 상성 관계입니다.
- 3번 (cbene > eyanoo)만 실제 데이터와 일치
