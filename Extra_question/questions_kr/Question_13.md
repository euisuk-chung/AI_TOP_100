# Question
에이전트가 행동 뒤에 숨겨진 추론 없이 행동합니다.

# Answer
Reason & Act (ReAct)

# Explanation
**문제 상황 (The Problem):**
에이전트가 단순히 "'Apple' 검색"을 출력한다면, *왜* 그런지 알 수 없습니다. 과일을 찾는 걸까요, 아니면 회사를 찾는 걸까요? 실수를 하더라도 "사고 과정"이 모델의 신경망 가중치 안에 숨겨져 있기 때문에 디버깅할 수 없습니다.

**해결책: ReAct (Reason + Act)**
ReAct는 모델이 모든 "Action(행동)" 전에 "Thought(생각)"를 출력하도록 강제합니다.
- **Thought**: "사용자가 주가에 대해 물었으므로 'Apple'은 AAPL 회사를 의미한다."
- **Action**: `search_stock("AAPL")`

이는 에이전트의 행동을 투명하고 해석 가능하게 만들며 논리적 비약이 발생할 가능성을 줄입니다.

**실제 기업 사례 (Real Enterprise Example):**
**사이버 보안 위협 사냥**: 보안 분석가는 ReAct 기반 에이전트를 사용하여 경고를 조사합니다. 단순히 스크립트를 실행하는 대신, 에이전트는 추론을 기록합니다: "Thought: IP 주소가 알려진 악성 블록에서 왔다. 내부 장치가 이 IP와 통신했는지 확인해야 한다. Action: `query_firewall_logs(ip)`." 이 감사 추적(audit trail)은 규정 준수와 나중에 인간 분석가가 사건을 이해하는 데 매우 중요합니다.
