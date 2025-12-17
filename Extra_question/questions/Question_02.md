# Question
Agents cannot connect insights across multiple reasoning branches.

# Answer
Graph of Thought

# Explanation
**The Problem:**
Standard "Chain of Thought" reasoning is linear: A -> B -> C. If the agent needs to combine an insight from path A (e.g., "The suspect was in London") with an insight from path B (e.g., "The murder weapon is sold only in Paris"), a linear chain might miss the connection if it doesn't explicitly backtrack and merge these ideas.

**The Solution: Graph of Thought (GoT)**
GoT models reasoning as a network (graph), not a line.
- **Nodes** are thoughts or information states.
- **Edges** are connections or dependencies.

This allows the agent to:
1. **Aggregate**: Combine results from three different brainstorming branches into one best solution.
2. **Loop**: Revisit a previous thought with new information.
3. **Branch**: Explore multiple possibilities in parallel and then merge the successful ones.

It's like a detective connecting photos on a wall with string—non-linear and relational.
