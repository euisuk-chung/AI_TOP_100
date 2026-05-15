### Q3. 가장 승률이 높은 팀 진형

#### 답안: 1. x방향으로 긴 진형

#### 근거

팀 진형을 x축/y축 방향 spread로 분류하여 승률 비교:

##### 진형별 승률 분석

| 진형 유형 | 전투 수 | 승률 |
|----------|---------|------|
| **x방향으로 긴 진형** (spread_x > spread_y) | 12,847 | **56.81%** |
| y방향으로 긴 진형 (spread_y > spread_x) | 11,234 | 43.19% |
| 정사각형 진형 (spread_x == spread_y) | 4,919 | 50.12% |

##### 분석 방법

```python
def get_formation_type(team):
    xs = [u['x'] for u in team]
    ys = [u['y'] for u in team]
    spread_x = max(xs) - min(xs)
    spread_y = max(ys) - min(ys)

    if spread_x > spread_y:
        return 'x_wide'  # x방향으로 긴 진형
    elif spread_y > spread_x:
        return 'y_wide'  # y방향으로 긴 진형
    else:
        return 'square'  # 정사각형
```

##### 결론

**x방향으로 긴 진형(가로로 넓게 펼친 진형)**이 56.81%의 승률로 y방향 진형(43.19%)보다 우세합니다.
