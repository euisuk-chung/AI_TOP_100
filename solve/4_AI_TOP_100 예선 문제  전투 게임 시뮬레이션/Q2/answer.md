### Q2. 배치 위치에 따른 승률 차이가 가장 큰 유닛

#### 답안: 3. eyanoo

#### 근거

전방(y >= 5) vs 후방(y < 5) 배치에 따른 승률 차이 분석:

##### 배치 위치별 승률 차이

| 유닛 | 전방 승률 | 후방 승률 | **차이(절대값)** |
|------|-----------|-----------|------------------|
| **eyanoo** | 57.65% | 26.53% | **31.12%** |
| bras | 49.93% | 34.11% | 15.82% |
| cbene | 52.15% | 38.47% | 13.68% |
| aleo | 51.89% | 40.23% | 11.66% |
| dgreg | 55.78% | 46.12% | 9.66% |

##### 분석 방법

```python
# 전방/후방 기준: y좌표 5 기준
FRONT_THRESHOLD = 5

for battle in train_battles:
    for team in ['red', 'blue']:
        for unit_data in battle[f'{team}_team']:
            is_front = unit_data['y'] >= FRONT_THRESHOLD
            is_win = (battle['winner'] == team)
            # 전방/후방별 승률 집계
```

**eyanoo**는 전방 배치 시 57.65%, 후방 배치 시 26.53%로 **31.12%** 차이를 보여 배치 효과가 가장 큽니다.
