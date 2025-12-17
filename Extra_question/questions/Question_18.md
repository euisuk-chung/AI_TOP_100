# Question
Agents forget what happened five minutes ago.

# Answer
Episodic Memory

# Explanation
**The Problem:**
LLMs have a fixed context window. As a conversation gets long, the beginning gets cut off. If you said "My name is Tom" at the start, 20 minutes later the agent might ask "Who are you?".

**The Solution: Episodic Memory**
Episodic Memory is like a diary or a log of the session.
- **Recording**: It saves key events: "User said name is Tom at 10:00 AM."
- **Recall**: Before answering, the agent checks the diary.
- **Result**: "I remember you said your name is Tom."
