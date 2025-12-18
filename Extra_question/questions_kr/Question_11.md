# Question
모델이 올바른 도구를 선택하지만, 유효한 도구 호출을 생성하지 못합니다.

# Answer
Function Calling

# Explanation
**문제 상황 (The Problem):**
LLM은 "5와 10의 합을 계산할게"라고 말할 수 있습니다. 이는 사람이 읽을 수는 있지만 컴퓨터 프로그램은 이 문장을 실행할 수 없습니다. 컴퓨터는 `add(5, 10)`이 필요합니다. 엄격한 형식이 없으면 에이전트의 의도가 번역 과정에서 손실됩니다.

**해결책: Function Calling**
Function Calling은 모델이 특정 스키마와 일치하는 구조화된 형식(JSON 등)으로 데이터를 출력하도록 강제합니다.
- **Schema (스키마)**: `function add(a: int, b: int)`를 정의합니다.
- **Output (출력)**: 모델은 `{"name": "add", "arguments": {"a": 5, "b": 10}}`를 생성합니다.
- **Execution (실행)**: 시스템은 이 JSON을 파싱하고 코드를 안정적으로 실행합니다.

**실제 기업 사례 (Real Enterprise Example):**
**HubSpot CRM 통합**: HubSpot은 사용자가 채팅을 통해 CRM과 상호 작용할 수 있도록 Function Calling을 사용합니다. 사용자가 "john@example.com의 John Doe에 대한 새 연락처를 만들어줘"라고 말하면, LLM은 단순히 "알겠습니다"라고 말하는 것이 아니라, 백엔드 시스템이 실제로 데이터베이스를 업데이트하기 위해 실행하는 구조화된 함수 호출 `create_contact(name="John Doe", email="john@example.com")`을 생성합니다.
