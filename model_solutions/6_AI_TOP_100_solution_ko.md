# 모범 답안: Q6. AI 입국 심사관

## 출제 의도

### 문제 패턴

**P4. 최적화/의사결정 (Decision)** - 제약 조건 하에서 목표를 최대화하는 최적의 의사결정을 내리는 시뮬레이션

### 핵심 측정 역량

1. **규칙 기반 로직 구현**: 복잡한 조건문을 정확하게 코드로 변환
2. **엣지 케이스 처리**: 예외 상황과 경계 조건 고려
3. **데이터 검증**: 입력 데이터의 유효성 확인
4. **명시적 검증 유도**: 승인/거부 결정과 사유 코드로 정확성 검증

### 왜 '딸깍'으로 풀리지 않는가?

- "이 신청자들 심사해줘"라고 하면 AI가 **규칙을 임의로 해석**할 수 있음
- 규칙의 **우선순위와 조합**이 결과에 영향 (여권 만료 vs 범죄 기록 중 뭐가 먼저?)
- 날짜 비교, 금액 기준 등 **정확한 계산**이 필요
- 새로운 규칙이 추가되면 **로직 수정 필요** - 유연한 설계 중요

### 난이도 구조

- **Q1-Q3 (Easy)**: 단일 조건 판단 - 기본 규칙 적용
- **Q4 (Medium)**: 복합 조건 - 여러 규칙 조합
- **Q5 (Hard)**: 예외 케이스 - 엣지 케이스 처리 (킬러 문항)

---

## 권장 접근법

### 1단계: 사람의 분석

- 심사 규칙을 명확히 정의하고 우선순위 결정
- 승인/거부 기준과 사유 코드 매핑
- 엣지 케이스 식별 (경계값, 특수 상황)

### 2단계: AI와의 협업

```text
프롬프트 예시:
"출입국 심사 로직을 Python으로 구현해줘.

입력: 신청자 목록 (JSON)
- id: 신청자 ID
- passport_expiry: 여권 만료일 (YYYY-MM-DD)
- visa_valid: 비자 유효 여부 (boolean)
- visa_expiry: 비자 만료일 (YYYY-MM-DD)
- criminal_record: 범죄 기록 여부 (boolean)
- funds: 보유 자금 (USD)
- purpose: 방문 목적

규칙 (우선순위 순):
1. 여권 만료 → 거부 (사유 1)
2. 비자 무효/만료 → 거부 (사유 2)
3. 범죄 기록 있음 → 거부 (사유 3)
4. 자금 < $1000 → 거부 (사유 4)
5. 목적 불명확 → 거부 (사유 5)
6. 모든 조건 통과 → 승인

출력: JSON 배열 [{id, answer, reason(거부시)}]"
```

### 3단계: 사람의 검증

1. **테스트 케이스 작성**: 각 거부 사유별 샘플 데이터
2. **경계값 테스트**: 만료일 당일, 자금 정확히 $1000 등
3. **복합 조건 테스트**: 여러 거부 사유가 동시에 해당될 때
4. **예상 결과와 실제 결과 대조**

---

## 기준 로직

### 승인 조건 (모두 충족)

- 여권 유효 (만료되지 않음)
- 비자 유효 (유형 일치, 만료되지 않음)
- 범죄 기록 없음
- 자금 >= 기준 (예: $1000)
- 목적 명확 (Tourism, Business, Study, Work 중 하나)

### 거부 사유 코드

| 코드 | 사유 | 우선순위 |
|------|------|----------|
| 1 | 만료된 여권 | 최우선 |
| 2 | 유효하지 않은/만료된 비자 | 2순위 |
| 3 | 범죄 기록 | 3순위 |
| 4 | 불충분한 자금 | 4순위 |
| 5 | 불명확한 목적 | 5순위 |

---

## 풀이 스크립트 (Python)

```python
import json
from datetime import datetime

def check_immigration(applicants, reference_date=None):
    """
    출입국 심사 로직

    Args:
        applicants: 신청자 목록 (JSON)
        reference_date: 기준일 (None이면 오늘)

    Returns:
        심사 결과 JSON 문자열
    """
    results = []
    current_date = reference_date or datetime.now().date()

    # 유효한 방문 목적
    VALID_PURPOSES = ["Tourism", "Business", "Study", "Work"]

    # 최소 자금 기준
    MIN_FUNDS = 1000

    for app in applicants:
        decision = "Approve"
        reason = None

        # 1. 여권 만료 확인 (최우선)
        passport_expiry = datetime.strptime(
            app['passport_expiry'], "%Y-%m-%d"
        ).date()

        if passport_expiry < current_date:
            decision = "Deny"
            reason = 1

        # 2. 비자 확인
        elif not app.get('visa_valid', False):
            decision = "Deny"
            reason = 2
        elif 'visa_expiry' in app:
            visa_expiry = datetime.strptime(
                app['visa_expiry'], "%Y-%m-%d"
            ).date()
            if visa_expiry < current_date:
                decision = "Deny"
                reason = 2

        # 3. 범죄 기록 확인
        elif app.get('criminal_record', False):
            decision = "Deny"
            reason = 3

        # 4. 자금 확인
        elif app.get('funds', 0) < MIN_FUNDS:
            decision = "Deny"
            reason = 4

        # 5. 방문 목적 확인
        elif app.get('purpose', '') not in VALID_PURPOSES:
            decision = "Deny"
            reason = 5

        # 결과 구성
        result = {"id": app['id'], "answer": decision}
        if decision == "Deny":
            result["reason"] = reason
        results.append(result)

    return json.dumps(results, indent=2)


# 테스트 케이스
def run_tests():
    """단위 테스트"""
    test_applicants = [
        {
            "id": "A001",
            "passport_expiry": "2024-01-01",  # 만료됨
            "visa_valid": True,
            "visa_expiry": "2025-12-31",
            "criminal_record": False,
            "funds": 5000,
            "purpose": "Tourism"
        },
        {
            "id": "A002",
            "passport_expiry": "2026-01-01",
            "visa_valid": False,  # 비자 무효
            "visa_expiry": "2025-12-31",
            "criminal_record": False,
            "funds": 5000,
            "purpose": "Tourism"
        },
        {
            "id": "A003",
            "passport_expiry": "2026-01-01",
            "visa_valid": True,
            "visa_expiry": "2025-12-31",
            "criminal_record": True,  # 범죄 기록
            "funds": 5000,
            "purpose": "Tourism"
        },
        {
            "id": "A004",
            "passport_expiry": "2026-01-01",
            "visa_valid": True,
            "visa_expiry": "2025-12-31",
            "criminal_record": False,
            "funds": 500,  # 자금 부족
            "purpose": "Tourism"
        },
        {
            "id": "A005",
            "passport_expiry": "2026-01-01",
            "visa_valid": True,
            "visa_expiry": "2025-12-31",
            "criminal_record": False,
            "funds": 5000,
            "purpose": "Unknown"  # 불명확한 목적
        },
        {
            "id": "A006",
            "passport_expiry": "2026-01-01",
            "visa_valid": True,
            "visa_expiry": "2025-12-31",
            "criminal_record": False,
            "funds": 5000,
            "purpose": "Business"  # 모든 조건 충족
        }
    ]

    # 기준일을 2025-01-01로 설정하여 테스트
    reference = datetime(2025, 1, 1).date()
    result = check_immigration(test_applicants, reference)
    print(result)

# 실행
# run_tests()
```

---

## 엣지 케이스 고려사항

### 경계값 처리

```python
# 만료일이 오늘인 경우
# - 당일까지 유효로 처리할지, 만료로 처리할지 명확히
if passport_expiry <= current_date:  # 당일도 만료
# vs
if passport_expiry < current_date:   # 당일은 유효
```

### 누락된 필드 처리

```python
# 필드가 없을 경우 기본값 사용
funds = app.get('funds', 0)  # 없으면 0으로 처리
visa_valid = app.get('visa_valid', False)  # 없으면 무효
```

### 복합 거부 사유

```python
# 여러 사유가 동시에 해당될 때 - 우선순위가 높은 것만 반환
# 예: 여권 만료 + 범죄 기록 → 사유 1 (여권 만료) 반환
```

---

## 핵심 교훈

> "규칙 기반 시스템은 **명확한 규칙 정의**와 **우선순위 결정**이 핵심이다. AI가 코드를 생성해주지만, **규칙의 해석과 엣지 케이스 처리**는 사람이 검토해야 한다."

이 문제는 규칙 기반 의사결정 시스템 구현에서 **정확한 요구사항 정의**와 **철저한 테스트**의 중요성을 보여줍니다. AI가 생성한 코드를 **테스트 케이스로 검증**하는 과정이 필수입니다.
