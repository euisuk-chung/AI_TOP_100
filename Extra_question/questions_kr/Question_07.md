# Question
에이전트가 존재하는지 몰랐던 경계를 넘습니다.

# Answer
Safety Guardrails

# Explanation
**문제 상황 (The Problem):**
자율 에이전트는 강력한 엔진과 같습니다. "불필요한 파일 삭제"를 지시하면, 운영 체제 파일을 "불필요"하다고 판단하여 삭제할 수도 있습니다. 알려주지 않는 한 무엇이 "금지 구역"인지 본질적으로 알지 못합니다.

**해결책: Safety Guardrails**
Guardrails(가드레일)는 볼링의 "범퍼"나 놀이터의 "울타리"와 같습니다.
- **Input Rails (입력 레일)**: 에이전트가 악의적인 프롬프트(예: "이전의 모든 지시 무시")를 처리하지 못하게 합니다.
- **Output Rails (출력 레일)**: 에이전트가 불쾌한 말을 하지 못하게 합니다.
- **Action Rails (행동 레일)**: 에이전트가 사람의 승인 없이 위험한 도구(예: `delete_database`)를 호출하지 못하게 합니다.

**실제 기업 사례 (Real Enterprise Example):**
**Microsoft Azure AI Content Safety**: Azure OpenAI Service를 사용하는 기업들은 탈옥 시도나 PII(개인 식별 정보) 유출을 자동으로 감지하고 차단하기 위해 가드레일을 구현합니다. 예를 들어, 은행 챗봇은 LLM이 도움이 되고 싶어서 고객의 전체 신용카드 번호를 확인해 주려고 하더라도, 이를 절대 출력하지 못하도록 엄격하게 차단하는 가드레일을 갖추고 있습니다.
