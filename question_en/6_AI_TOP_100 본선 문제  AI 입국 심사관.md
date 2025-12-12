# AI_TOP_100 Final Round: AI Immigration Officer

Source: https://brunch.co.kr/@andkakao/327

### **Problem Description**

Review immigration applications and determine approval or denial based on the given criteria.

You are an AI immigration officer. You need to review immigration applications and determine whether to approve or deny them based on the following criteria:

**Approval Criteria:**
1. Valid passport (not expired)
2. Valid visa (appropriate type and not expired)
3. No criminal record
4. Sufficient funds for the stay
5. Clear purpose of visit

**Denial Reasons:**
1. Expired passport
2. Invalid or expired visa
3. Criminal record
4. Insufficient funds
5. Unclear purpose of visit

Review each application and make a decision.

### **Notes and References**

Follow the specified JSON format to submit the results.

### **Sample Problem Materials**

![Screenshot](//img1.daumcdn.net/thumb/R1280x0.fpng/?fname=http://t1.daumcdn.net/brunch/service/user/41jj/image/kBnegNtQTvn7yifOPikOviYZOII.png) 

This data can be found on the problem-solving website to be released later.

---

### Q. Submit the examination results for 30 immigration applicants in the format below.

Submission Format: A single JSON array that satisfies the schema below

- id: Examination ID (e.g., applicant_001)
- answer: Approval/Denial decision (Approve or Deny, case-sensitive)
- reason: Denial reason number if Deny (number)

> ```json
> [
>   {
>     "id": "applicant_001",
>     "answer": "Approve"
>   },
>   {
>     "id": "applicant_002",
>     "answer": "Deny",
>     "reason": 3
>   }
> ]
> ```
