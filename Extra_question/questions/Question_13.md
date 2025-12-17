# Question
Agents act with no reasoning behind the action.

# Answer
Reason & Act (ReAct)

# Explanation
**The Problem:**
If an agent just outputs "Search for 'Apple'", you don't know *why*. Is it looking for the fruit or the company? If it makes a mistake, you can't debug it because the "thought process" is hidden inside the model's neural weights.

**The Solution: ReAct (Reason + Act)**
ReAct forces the model to output a "Thought" before every "Action".
- **Thought**: "The user asked about stock prices, so 'Apple' refers to the company AAPL."
- **Action**: `search_stock("AAPL")`

This makes the agent's behavior transparent, interpretable, and less prone to logical leaps.
