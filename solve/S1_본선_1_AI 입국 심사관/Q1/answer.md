### Q1. AI 입국 심사관 - 30명 승인/거부 판정

#### 답안: results_v2.json 참조 (승인 10명, 거부 20명)

#### 근거

##### 문제 요약
30명의 입국 신청자에 대해 25개 규칙을 적용하여 승인/거부 판정

##### 풀이 방법
1. 여권 이미지 수동 OCR → `passport_data.json` 생성
2. `immigration_check_v2.py`로 25개 규칙 검사
3. 무비자 협정국 처리:
   - Kingdom of Neverland: 30일
   - Federation of Serenia: 60일
   - Republic of Valeria: 90일

##### 결과
- **승인 (Approve)**: 10명
- **거부 (Deny)**: 20명

###### 주요 거부 사유
| 규칙 | 사유 | 해당자 수 |
|:---:|:---|:---:|
| 8 | 이름 불일치 | 다수 |
| 13 | 여권 만료 | applicant_013 |

##### 최종 답안
`results_v2.json` 참조

```json
[
  {"id": "applicant_001", "answer": "Approve"},
  {"id": "applicant_002", "answer": "Deny", "reason": 8},
  ...
]
```
