# Question
The model selects the right tool, but doesn’t produce a valid tool call.

# Answer
Function Calling

# Explanation
Agents may select the right tool, but the LLM may fail to emit the tool call in a machine-executable format. Function Calling fixes this by requiring the model to follow a strict schema, ensuring tool calls include the correct arguments.
