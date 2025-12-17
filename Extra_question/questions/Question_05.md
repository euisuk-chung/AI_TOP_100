# Question
Agents cannot reason over relationships between retrieved documents.

# Answer
Graph RAG

# Explanation
**The Problem:**
Standard RAG retrieves documents based on keyword similarity. If Document A mentions "Project X" and Document B mentions that "Project X was delayed", but neither document mentions "Delay causes", a standard RAG might miss the connection. It sees "dots" but not the lines connecting them.

**The Solution: Graph RAG**
Graph RAG uses a Knowledge Graph to structure data before retrieval.
- **Entities**: People, Places, Concepts (Nodes).
- **Relationships**: "Works for", "Located in", "Caused by" (Edges).

When you ask a question, it traverses this graph. It can find answers that require "multi-hop" reasoning, like "Who is the manager of the person who wrote the delayed report?", even if that answer spans across three different documents.
