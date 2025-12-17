# Question
Agents cannot generalize to new instructions.

# Answer
LLM Agent

# Explanation
**The Problem:**
Old-school "chatbots" or scripts follow strict if-then rules. If you ask a "Refund Bot" to "Help me return this item because it's broken," it works. If you ask "I bought this, but it's shattered, what do I do?", a rule-based bot might fail if it doesn't have a rule for "shattered".

**The Solution: LLM Agent**
An LLM Agent uses a Large Language Model as its brain.
- **Reasoning**: It understands that "shattered" implies "broken" and "return".
- **Adaptability**: It can handle instructions it has never seen before by using common sense.
- **Tool Use**: It decides *which* rule or tool to apply based on understanding, not just keyword matching.
