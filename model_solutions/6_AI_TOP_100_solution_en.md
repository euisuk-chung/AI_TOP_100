# Model Solution: Q6. AI Immigration Officer

## Problem Pattern

**P4. Optimization/Decision Making (Decision)** - Simulation to make optimal decisions maximizing goals under constraints

## Key Competencies

1. **Rule-based Logic Implementation**: Accurately convert complex conditions into code
2. **Edge Case Handling**: Consider exceptions and boundary conditions
3. **Data Validation**: Verify input data validity
4. **Explicit Verification**: Verify accuracy through approval/denial decisions and reason codes

## Why Can't This Be Solved with a Single Click?

- Asking "review these applicants" may lead AI to **arbitrarily interpret rules**
- **Rule priority and combination** affect results (passport expiry vs criminal record - which first?)
- **Precise calculations** needed for date comparisons, amount thresholds
- When new rules are added, **logic modification needed** - flexible design important

---

## Recommended Approach

### Step 1: Human Analysis

- Clearly define review rules and determine priorities
- Map approval/denial criteria to reason codes
- Identify edge cases (boundary values, special situations)

### Step 2: AI Collaboration

```text
Example Prompt:
"Implement immigration review logic in Python.

Input: Applicant list (JSON)
- id: Applicant ID
- passport_expiry: Passport expiry date (YYYY-MM-DD)
- visa_valid: Visa validity (boolean)
- visa_expiry: Visa expiry date (YYYY-MM-DD)
- criminal_record: Criminal record (boolean)
- funds: Available funds (USD)
- purpose: Visit purpose

Rules (by priority):
1. Passport expired → Deny (reason 1)
2. Visa invalid/expired → Deny (reason 2)
3. Has criminal record → Deny (reason 3)
4. Funds < $1000 → Deny (reason 4)
5. Unclear purpose → Deny (reason 5)
6. All conditions passed → Approve

Output: JSON array [{id, answer, reason(if denied)}]"
```

### Step 3: Human Verification

1. **Test cases**: Sample data for each denial reason
2. **Boundary testing**: Expiry date today, exactly $1000 funds, etc.
3. **Compound condition testing**: Multiple denial reasons apply simultaneously
4. **Compare expected vs actual results**

---

## Criteria Logic

### Approval Conditions (All must be met)

- Passport valid (not expired)
- Visa valid (type match, not expired)
- No criminal record
- Funds >= threshold (e.g., $1000)
- Purpose clear (Tourism, Business, Study, Work)

### Denial Reason Codes

| Code | Reason | Priority |
|------|--------|----------|
| 1 | Expired passport | Highest |
| 2 | Invalid/expired visa | 2nd |
| 3 | Criminal record | 3rd |
| 4 | Insufficient funds | 4th |
| 5 | Unclear purpose | 5th |

---

## Solution Script (Python)

```python
import json
from datetime import datetime

def check_immigration(applicants, reference_date=None):
    """
    Immigration review logic

    Args:
        applicants: Applicant list (JSON)
        reference_date: Reference date (None = today)

    Returns:
        Review result JSON string
    """
    results = []
    current_date = reference_date or datetime.now().date()

    # Valid visit purposes
    VALID_PURPOSES = ["Tourism", "Business", "Study", "Work"]

    # Minimum funds threshold
    MIN_FUNDS = 1000

    for app in applicants:
        decision = "Approve"
        reason = None

        # 1. Passport expiry check (highest priority)
        passport_expiry = datetime.strptime(
            app['passport_expiry'], "%Y-%m-%d"
        ).date()

        if passport_expiry < current_date:
            decision = "Deny"
            reason = 1

        # 2. Visa check
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

        # 3. Criminal record check
        elif app.get('criminal_record', False):
            decision = "Deny"
            reason = 3

        # 4. Funds check
        elif app.get('funds', 0) < MIN_FUNDS:
            decision = "Deny"
            reason = 4

        # 5. Visit purpose check
        elif app.get('purpose', '') not in VALID_PURPOSES:
            decision = "Deny"
            reason = 5

        # Build result
        result = {"id": app['id'], "answer": decision}
        if decision == "Deny":
            result["reason"] = reason
        results.append(result)

    return json.dumps(results, indent=2)
```

---

### Q1. Review Results for 30 Applicants

**Approach**: Understand 25 detailed regulations and implement a system that automatically validates 7 types of immigration documents (passport, visa, entry form, etc.) according to rules.

**Guide**:

1. **Rule file analysis**: Extract 25 rules from `inspection_rules.txt` and determine priorities
2. **Data loading**: Parse 30 applicants' document data as JSON
3. **Apply rules**: Validate each applicant sequentially from rule 1
4. **Generate results**: On violation, deny with first (lowest number) violated rule as reason

**Key Rule Examples** (refer to `inspection_rules.txt` for actual rules):

- Rule 1: Passport must have 6+ months validity from inspection date
- Rule 2: Visa type must match visit purpose
- Rule 3: All required fields in entry form must be completed
- Rule 4: Planned stay duration must be within visa allowed period
- ...

**Verification Checklist**:

- [ ] Check passport validity (based on inspection date 2025-11-22)
- [ ] Verify visa type and purpose match
- [ ] Check for missing required documents
- [ ] Verify numerical criteria (amounts, durations) are met
- [ ] Return lowest rule number for multiple violations

**Answer Format**: JSON array of review results for all 30 applicants

```json
[
  {"id": "applicant_001", "answer": "Approve"},
  {"id": "applicant_002", "answer": "Deny", "reason": 3},
  {"id": "applicant_003", "answer": "Deny", "reason": 7},
  {"id": "applicant_004", "answer": "Approve"},
  ...
]
```

**Answer**: Analyze provided `applicants.json` and `inspection_rules.txt`, applying all 25 rules accurately. Actual answer depends on specific data file contents.

---

## Edge Case Considerations

### Boundary Value Handling

```python
# When expiry date is today
# - Clarify if same day is valid or expired
if passport_expiry <= current_date:  # Same day = expired
# vs
if passport_expiry < current_date:   # Same day = valid
```

### Missing Field Handling

```python
# Use defaults when fields are missing
funds = app.get('funds', 0)  # Treat missing as 0
visa_valid = app.get('visa_valid', False)  # Treat missing as invalid
```

### Multiple Denial Reasons

```python
# When multiple reasons apply - return only highest priority
# e.g., Passport expired + Criminal record → reason 1 (passport expired)
```

---

## Key Lesson

> "Rule-based systems require **clear rule definition** and **priority decisions**. AI can generate code, but **rule interpretation and edge case handling** require human review."

This problem shows the importance of **precise requirements definition** and **thorough testing** in implementing rule-based decision systems. **Verifying AI-generated code with test cases** is essential.
