# 모범 답안: Q8. AI 출입국 심사관

## 분석
**목표**: 출입국 신청자의 규칙 기반 분류.
**입력**: 신청자 목록 (JSON).
**출력**: 승인/거부 결정과 사유 코드.

## 기준 로직
**승인**:
-   여권 유효 (만료되지 않음)
-   비자 유효 (유형 일치, 만료되지 않음)
-   범죄 기록 없음
-   자금 >= 기준 (예: $1000 또는 체류에 충분한 금액)
-   목적 명확

**거부 사유**:
1.  만료된 여권
2.  유효하지 않은/만료된 비자
3.  범죄 기록
4.  불충분한 자금
5.  불명확한 목적

## 풀이 스크립트 (Python)

```python
import json
from datetime import datetime

def check_immigration(applicants):
    results = []
    current_date = datetime.now().date() # 또는 특정 시뮬레이션 날짜

    for app in applicants:
        decision = "Approve"
        reason = None

        # 1. 여권 확인
        passport_expiry = datetime.strptime(app['passport_expiry'], "%Y-%m-%d").date()
        if passport_expiry < current_date:
            decision = "Deny"
            reason = 1

        # 2. 비자 확인
        elif not app['visa_valid'] or datetime.strptime(app['visa_expiry'], "%Y-%m-%d").date() < current_date:
            decision = "Deny"
            reason = 2

        # 3. 범죄 기록
        elif app['criminal_record']:
            decision = "Deny"
            reason = 3

        # 4. 자금 확인
        elif app['funds'] < 1000: # $1000 기준 가정
            decision = "Deny"
            reason = 4

        # 5. 목적 확인
        elif app['purpose'] not in ["Tourism", "Business", "Study", "Work"]:
            decision = "Deny"
            reason = 5

        # 결과 구성
        res = {"id": app['id'], "answer": decision}
        if decision == "Deny":
            res["reason"] = reason
        results.append(res)

    return json.dumps(results, indent=2)

# 사용 예시
# print(check_immigration(json_data))
```
