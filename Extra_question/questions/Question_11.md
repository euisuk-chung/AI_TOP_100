# Question
The model selects the right tool, but doesn’t produce a valid tool call.

# Answer
Function Calling

# Explanation
**The Problem:**
An LLM might say, "I'll calculate the sum of 5 and 10." This is human-readable, but a computer program can't execute that sentence. It needs `add(5, 10)`. Without a strict format, the agent's intent is lost in translation.

**The Solution: Function Calling**
Function Calling forces the model to output data in a structured format (like JSON) that matches a specific schema.
- **Schema**: You define `function add(a: int, b: int)`.
- **Output**: The model generates `{"name": "add", "arguments": {"a": 5, "b": 10}}`.
- **Execution**: The system parses this JSON and runs the code reliably.
