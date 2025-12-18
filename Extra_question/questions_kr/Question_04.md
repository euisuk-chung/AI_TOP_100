# Question
에이전트가 일관성 없는 방식으로 도구와 데이터에 접근합니다.

# Answer
Model Control Protocol (MCP)

# Explanation
**문제 상황 (The Problem):**
에이전트를 Google Drive에 연결하려면 특정 코드를 작성해야 합니다. Slack에 연결하려면 다른 코드를 작성해야 합니다. 로컬 데이터베이스에 연결하려면 또 다른 코드가 필요합니다. 이러한 "스파게티 통합"은 유지 관리하기 어렵고 보안에 취약합니다.

**해결책: Model Control Protocol (MCP)**
MCP는 AI를 위한 USB와 같은 표준입니다.
- **Universal Standard (보편적 표준)**: *어떤* 에이전트든 *어떤* 데이터 소스나 도구와도 대화할 수 있는 단일 방식을 정의합니다.
- **Security (보안)**: 권한(예: "읽기 전용" 액세스)을 위한 일관된 계층을 제공합니다.
- **Portability (이식성)**: Claude에서 GPT-4로 전환하더라도 도구 통합을 다시 작성할 필요가 없습니다.

이는 복잡한 커스텀 커넥터들을 깔끔한 플러그 앤 플레이 생태계로 바꿔줍니다.

**실제 기업 사례 (Real Enterprise Example):**
**Block (구 Square)**: Block은 Snowflake, Jira, Slack을 포함한 내부 엔지니어링 도구에 MCP를 통합했습니다. 각 도구마다 커스텀 챗봇을 만드는 대신, MCP를 사용하여 이 모든 시스템에 안전하게 액세스하는 단일 내부 에이전트("Goose")를 구축했습니다. 이를 통해 개발자들은 "최신 Snowflake 알림과 관련된 Jira 티켓의 상태는 어때?"라고 물을 수 있고, 표준화된 프로토콜을 통해 두 시스템 모두에서 정보를 가져오는 답변을 받을 수 있습니다.
