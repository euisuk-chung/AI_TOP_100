# Question
Agents give shallow replies that skip important steps.

# Answer
Chain of Thought (CoT)

# Explanation
**The Problem:**
LLMs are like students who try to guess the answer without doing the math. If asked "If I have 3 apples and buy 2 more, then eat 1, how many do I have?", a model might guess "5" because it sees numbers 3 and 2.

**The Solution: Chain of Thought**
CoT forces the model to "show its work".
- **Prompt**: "Let's think step by step."
- **Output**: "Start with 3. Buy 2 -> 3+2=5. Eat 1 -> 5-1=4. The answer is 4."

By generating the intermediate steps, the model grounds its final answer in logic, significantly reducing calculation and reasoning errors.
