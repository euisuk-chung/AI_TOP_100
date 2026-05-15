### Q3. 유적의 문 열기 (힌트: 멈추어야 비로소 보이리라)

#### 답안: POTS

#### 근거

##### 힌트 해석

- "멈추어야 비로소 보이리라" → **STOP** 입력
- "스스로를 되돌아보는 주문" → 뒤집기 처리

##### 코드 로직

```python
user_input = "STOP"
result = user_input[::-1].upper()  # 뒤집고 대문자로
print(result)  # POTS
```

##### 계산

| 단계 | 값 |
|------|-----|
| 입력 | `STOP` |
| 뒤집기 | `POTS` |
| 대문자 | `POTS` (변화 없음) |

##### TURNAROUND의 의미

코드 첫줄에 있는 `r=lambda x:input("TURNAROUND")`에서 "TURNAROUND"는:
- 영어로 "돌아서다", "뒤집다"의 의미
- 입력값을 뒤집어서(reverse) 출력하라는 힌트

