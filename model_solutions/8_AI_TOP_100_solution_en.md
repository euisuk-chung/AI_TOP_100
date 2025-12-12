# Model Solution: Q8. AI Immigration Officer

## Analysis
**Goal**: Rule-based classification of immigration applicants.
**Input**: List of applicants (JSON).
**Output**: Approval/Denial decision with reason code.

## Criteria Logic
**Approve**:
-   Passport Valid (not expired)
-   Visa Valid (type match, not expired)
-   No Criminal Record
-   Funds >= Threshold (e.g., $1000 or sufficient for stay)
-   Purpose Clear

**Deny Reasons**:
1.  Expired Passport
2.  Invalid/Expired Visa
3.  Criminal Record
4.  Insufficient Funds
5.  Unclear Purpose

## Solution Script (Python)

```python
import json
from datetime import datetime

def check_immigration(applicants):
    results = []
    current_date = datetime.now().date() # Or specific simulation date
    
    for app in applicants:
        decision = "Approve"
        reason = None
        
        # 1. Passport Check
        passport_expiry = datetime.strptime(app['passport_expiry'], "%Y-%m-%d").date()
        if passport_expiry < current_date:
            decision = "Deny"
            reason = 1
            
        # 2. Visa Check
        elif not app['visa_valid'] or datetime.strptime(app['visa_expiry'], "%Y-%m-%d").date() < current_date:
            decision = "Deny"
            reason = 2
            
        # 3. Criminal Record
        elif app['criminal_record']:
            decision = "Deny"
            reason = 3
            
        # 4. Funds Check
        elif app['funds'] < 1000: # Assuming $1000 threshold
            decision = "Deny"
            reason = 4
            
        # 5. Purpose Check
        elif app['purpose'] not in ["Tourism", "Business", "Study", "Work"]:
            decision = "Deny"
            reason = 5
            
        # Construct Result
        res = {"id": app['id'], "answer": decision}
        if decision == "Deny":
            res["reason"] = reason
        results.append(res)
        
    return json.dumps(results, indent=2)

# Example Usage
# print(check_immigration(json_data))
```
