# 20 Core Agentic AI Concepts Review

## 1. LLM Agent
**Definition**: An autonomous system that uses a Large Language Model (LLM) as its central "brain" to perceive, reason, and act to achieve goals.
**Why it matters**: Traditional software follows rigid, pre-programmed rules. LLM Agents can handle ambiguity, adapt to new instructions, and solve open-ended problems by leveraging the general reasoning capabilities of LLMs.
**How it works**: The agent receives a task, uses the LLM to break it down into steps, decides which tools to use, executes actions, and observes the results to proceed further.
**Example**: A "Customer Service Agent" that reads a user's complaint, checks the database for order details, decides whether to issue a refund or ask for more info, and drafts a polite email response—all without a specific script for every scenario.

## 2. Tool Use
**Definition**: The capability of an AI agent to utilize external software, APIs, or utilities to perform actions in the real world.
**Why it matters**: LLMs are text-in, text-out engines isolated from the world. Tool use bridges this gap, allowing them to actually *do* things like searching the web, querying databases, or calculating numbers, rather than just hallucinating answers.
**How it works**: The agent selects a tool from a provided list, generates the necessary inputs (arguments), and the system executes the tool and feeds the output back to the agent.
**Example**: An agent calculating "1234 * 5678" doesn't guess the number; it uses a `calculator` tool to get the exact result.

## 3. Function Calling
**Definition**: A structured way for an LLM to request the execution of a specific function with precise arguments, formatted typically as JSON.
**Why it matters**: It converts natural language intent into machine-readable code. Without it, an agent might say "Please run the search function for 'cats'", which a program can't execute. Function calling ensures the output is `search(query="cats")`.
**How it works**: The model is fine-tuned or prompted to output a specific schema (like JSON) when it wants to use a tool. The system parses this structured output to execute the code.
**Example**: When asked "What's the weather in Seoul?", the model outputs `{"function": "get_weather", "parameters": {"location": "Seoul"}}` instead of a sentence.

## 4. Reason-and-Act (ReAct)
**Definition**: A prompting framework where the agent explicitly generates a "Thought" (reasoning) before generating an "Action" (tool call).
**Why it matters**: It prevents impulsive actions. By forcing the model to "think out loud" first, it grounds the action in logic and allows for self-correction before the action is taken.
**How it works**: The prompt structure enforces a loop: `Thought` -> `Action` -> `Observation` -> `Thought`...
**Example**: 
*   **Thought**: "I need to find the user's IP address first."
*   **Action**: `get_user_info(user_id="123")`
*   **Observation**: "IP: 192.168.1.1"
*   **Thought**: "Now I can check the location for this IP."

## 5. Chain of Thought (CoT)
**Definition**: A technique where the model is prompted to generate intermediate reasoning steps before giving the final answer.
**Why it matters**: LLMs struggle with complex logic if forced to answer immediately. Breaking the problem down step-by-step significantly improves accuracy on math, logic, and planning tasks.
**How it works**: Using prompts like "Let's think step by step", the model outputs a sequence of logical deductions leading to the conclusion.
**Example**: Instead of just answering "42", the model says: "First, we calculate X... Then, we apply Y... Therefore, the result is 42."

## 6. Agent Loop
**Definition**: The continuous cycle of observation, reasoning, action, and feedback that keeps an agent running until a task is complete.
**Why it matters**: Real-world tasks are rarely "one-shot". Things change, actions fail, or new info appears. The loop allows the agent to persist and adapt over time.
**How it works**: It's a `while` loop in code: `while not done: state = observe(); action = decide(state); execute(action)`.
**Example**: A coding agent writes code, runs it, sees an error (feedback), rewrites the code, runs it again, and succeeds. The loop enables this trial-and-error.

## 7. Reflection
**Definition**: A process where the agent reviews its past actions or outputs to identify errors and areas for improvement.
**Why it matters**: It allows for self-correction. Instead of blindly repeating a mistake, the agent "looks back" to understand what went wrong and plans a better approach.
**How it works**: The agent is prompted with its previous failed attempt and asked, "What went wrong and how can you fix it?" before trying again.
**Example**: An agent writes an essay, then reads it to critique the flow and grammar, and finally rewrites a polished version.

## 8. Critic
**Definition**: A separate model or prompt role designed specifically to evaluate the quality, safety, or correctness of an agent's output.
**Why it matters**: Generating and verifying are different skills. A dedicated critic provides an objective "second opinion" or "preference signal" that the acting agent might miss.
**How it works**: Agent A generates a solution. Agent B (Critic) scores it or lists issues. Agent A uses this feedback to improve.
**Example**: A "Code Reviewer" agent that doesn't write code but checks the "Developer" agent's code for bugs and security flaws.

## 9. Plan-and-Execute
**Definition**: A strategy where the agent first creates a complete, high-level plan of all necessary steps and then executes them one by one.
**Why it matters**: It prevents the agent from getting lost in the details or going down a rabbit hole. It separates high-level strategy from low-level execution.
**How it works**: 
1.  **Planner**: Generates a list: "1. Search Google, 2. Summarize results, 3. Email summary."
2.  **Executor**: Takes item 1, does it. Takes item 2, does it.
**Example**: Writing a book: First outline the chapters (Plan), then write each chapter (Execute).

## 10. Episodic Memory
**Definition**: The ability to store and recall specific past events, actions, and observations from the current or recent sessions.
**Why it matters**: It gives the agent a sense of "now" and "what just happened". Without it, the agent would repeat the same search or forget user instructions given 5 minutes ago.
**How it works**: Storing the conversation history or a log of tool outputs in a list that is fed back into the prompt context.
**Example**: "I remember you asked me to save the file as 'report.pdf' three turns ago, so I will use that filename."

## 11. Semantic Memory
**Definition**: Long-term storage of facts, concepts, and knowledge that retrieves information based on meaning rather than exact keywords.
**Why it matters**: It allows agents to learn and retain vast amounts of knowledge (like company policies or entire codebases) that don't fit in the context window.
**How it works**: Text is converted into vectors (embeddings) and stored in a vector database. The agent queries this DB to find "relevant" info.
**Example**: An agent answering "What is our refund policy?" by retrieving the relevant paragraph from a 100-page PDF stored in vector memory.

## 12. Context Selection
**Definition**: The process of intelligently choosing exactly which pieces of information to include in the LLM's limited context window.
**Why it matters**: Context windows are limited and expensive. Dumping everything in confuses the model ("lost in the middle" phenomenon). Selecting only the *relevant* bits improves focus and accuracy.
**How it works**: Algorithms rank pieces of information by relevance (e.g., using embeddings or keyword matching) and keep only the top N items.
**Example**: When answering a question about "Chapter 5", the system only loads the text of Chapter 5 into the prompt, ignoring Chapters 1-4 and 6-10.

## 13. RAG (Retrieval-Augmented Generation)
**Definition**: A framework that retrieves relevant external data and provides it to the LLM to generate an answer grounded in that specific data.
**Why it matters**: It solves the "knowledge cutoff" and "hallucination" problems. The LLM doesn't need to memorize the world; it just needs to process the fresh data you give it.
**How it works**: User Query -> Search Database -> Retrieve Documents -> Paste into Prompt -> LLM Generates Answer based on Documents.
**Example**: A legal bot that searches a database of current laws to answer a specific case question, rather than relying on what it learned during training years ago.

## 14. Tree of Thought (ToT)
**Definition**: A reasoning framework where the agent explores multiple possible "branches" of reasoning simultaneously, evaluating each to find the best path.
**Why it matters**: Standard reasoning is linear. If the first step is wrong, the whole result is wrong. ToT allows "backtracking" and exploring alternatives, like a chess player considering multiple moves.
**How it works**: The model generates 3 possible next steps, evaluates which is most promising, and proceeds from there.
**Example**: Solving a riddle: "Option A leads to a contradiction. Option B looks good. Option C is impossible. Let's follow Option B."

## 15. Graph of Thought (GoT)
**Definition**: An extension of ToT where reasoning steps are modeled as a graph, allowing information to be combined, looped, and aggregated non-linearly.
**Why it matters**: Complex thoughts aren't just trees; they are networks. Insights from one branch can help another. GoT allows for the most flexible and complex reasoning structures.
**How it works**: Arbitrary connections between "thought nodes". A thought can merge with another, or loop back to refine a previous thought.
**Example**: Writing a novel: Character A's plot (Branch 1) and Character B's plot (Branch 2) merge in Chapter 5 (Node 3) to create a climax.

## 16. Graph RAG
**Definition**: A RAG approach that uses Knowledge Graphs to understand the *relationships* between entities in the retrieved data, not just the text chunks.
**Why it matters**: Standard RAG misses the "big picture" connections. Graph RAG can answer "How does X relate to Y?" even if they are never mentioned in the same document.
**How it works**: Data is structured as nodes (entities) and edges (relationships). The retrieval traverses this graph to find connected concepts.
**Example**: "What is the connection between Apple and OpenAI?" Graph RAG finds: Apple -> partners with -> OpenAI, even if no single news article explicitly summarizes the partnership depth.

## 17. Delegation
**Definition**: The practice of a main agent assigning specific sub-tasks to other specialized agents or workers.
**Why it matters**: One agent can't be an expert at everything. Specialization improves quality. It also allows for parallel processing.
**How it works**: A "Manager" agent identifies a coding task and sends it to a "Coder" agent, and a writing task to a "Writer" agent.
**Example**: A "CEO Agent" asks the "Research Agent" to find data and the "Chart Agent" to visualize it, then combines the results.

## 18. Orchestration
**Definition**: The management layer that coordinates the flow of data, execution order, and interaction between multiple agents and tools.
**Why it matters**: Without orchestration, multi-agent systems are chaos. Orchestration ensures tasks happen in the right order and data flows correctly from A to B.
**How it works**: A central control script or "Orchestrator Agent" manages the state, handles errors, and routes messages.
**Example**: A workflow engine that triggers the "Deploy" agent only *after* the "Test" agent reports 100% success.

## 19. Model Control Protocol (MCP)
**Definition**: A standardized open protocol that defines how AI models interact with content repositories, business tools, and development environments.
**Why it matters**: Currently, every integration is custom (one for Google Drive, one for Slack, etc.). MCP aims to be the "USB-C for AI apps"—write the integration once, and any MCP-compliant agent can use it.
**How it works**: It provides a universal interface for discovering resources, reading data, and calling tools, regardless of the underlying system.
**Example**: You install an "MCP Server" for your file system. Now, Claude, ChatGPT, and your local agent can all read/write files using the exact same standard commands.

## 20. Safety Guardrails
**Definition**: Rules, filters, and checks placed around an AI system to prevent it from generating harmful content, executing dangerous actions, or leaking sensitive data.
**Why it matters**: Autonomous agents can be dangerous if they go "off the rails" (e.g., deleting a production database). Guardrails ensure they stay within safe bounds.
**How it works**: Input/Output filters (checking for PII), permission scopes (read-only access), and "human-in-the-loop" approval steps.
**Example**: An agent tries to execute `DROP TABLE users`. The guardrail intercepts this SQL command, recognizes it as destructive, and blocks it, returning an error to the agent.
