# Question
Agents grab too much irrelevant text into the prompt.

# Answer
Context Selection

# Explanation
Agents may pull in too much text because they lack a way to decide what information is relevant for the current step. Context selection addresses this by deliberately choosing which pieces of retrieved text, memory, or prior interaction enter the prompt. Instead of loading entire documents or full conversation histories, only the most relevant information is included, keeping the prompt focused, compact, and easier for the agent to reason over.
