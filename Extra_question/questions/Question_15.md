# Question
Agents grab too much irrelevant text into the prompt.

# Answer
Context Selection

# Explanation
**The Problem:**
LLMs have a limited "Context Window" (like short-term memory). If you dump a whole 500-page book into the prompt to answer one specific question, the model gets overwhelmed, costs increase, and accuracy drops ("Lost in the Middle" phenomenon).

**The Solution: Context Selection**
This is the art of "packing light".
- **Filter**: Use search or embeddings to find only the 3 most relevant pages out of 500.
- **Inject**: Put only those 3 pages into the prompt.
- **Result**: The model focuses on the right info without distraction.
