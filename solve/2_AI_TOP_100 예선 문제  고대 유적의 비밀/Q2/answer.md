### Q2. 코드 실행 결과 (입력: 1q2w3e4r)

#### 답안: R4E3W2Q1

#### 근거

##### 코드 로직 분석

이미지의 Python 코드는 다음과 같이 동작합니다:

1. `i = input` - input 함수를 i에 할당
2. `p = lambda x: print(x, end="") or exit()` - 출력 후 종료 함수
3. 입력을 받음
4. **TURNAROUND** (뒤집기) 처리
5. 대문자 변환
6. 출력

##### 힌트 해석

- 첫줄: `r=lambda x:input("TURNAROUND")` - "TURNAROUND" = 뒤집기
- 석판 옆 힌트: "스스로를 되돌아보는 주문" = 뒤집기(reverse)

##### 계산

```python
user_input = "1q2w3e4r"
result = user_input[::-1].upper()  # 뒤집고 대문자로
print(result)  # R4E3W2Q1
```

| 단계 | 값 |
|------|-----|
| 입력 | `1q2w3e4r` |
| 뒤집기 | `r4e3w2q1` |
| 대문자 | `R4E3W2Q1` |

