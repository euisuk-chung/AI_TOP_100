### Q1. 1v1 전투에서 가장 높은 승률을 기록한 유닛

#### 답안: 4. dgreg

#### 근거

train_battles.json에서 1v1 전투(양팀 각 1유닛)를 필터링하여 각 유닛의 승률 분석:

##### 1v1 전투 승률 (총 3,020 경기)

| 유닛 | 승리 | 패배 | 승률 |
|------|------|------|------|
| **dgreg** | 455 | 147 | **75.58%** |
| cbene | 422 | 185 | 69.52% |
| aleo | 393 | 211 | 65.07% |
| eyanoo | 372 | 238 | 60.98% |
| bras | 368 | 229 | 61.64% |

##### 분석 방법

```python
# 1v1 전투 필터링
battles_1v1 = [b for b in train_battles
               if len(b['red_team']) == 1 and len(b['blue_team']) == 1]

# 유닛별 승률 계산
for battle in battles_1v1:
    winner_team = battle['winner']
    if winner_team == 'red':
        unit = battle['red_team'][0]['unit']
    else:
        unit = battle['blue_team'][0]['unit']
    # 승리 카운트
```

**dgreg**이 75.58%로 가장 높은 1v1 승률을 기록하여 1대1 최강자입니다.
