# Question
Agents tell me what to do but can't do it for me.

# Answer
Tool Use

# Explanation
**The Problem:**
A "Cooking Assistant" that says "Step 1: Turn on the oven" is helpful. But a "Smart Home Agent" that says "You should turn on the oven" is annoying—you want it to *do* it. Text-only models are trapped in a box; they can speak but not touch.

**The Solution: Tool Use**
Tool Use gives the agent "hands".
- **Capability**: The agent has a function `turn_on_oven()`.
- **Action**: Instead of outputting text, it outputs a command to trigger that function.
- **Result**: The oven actually turns on.

**Real Enterprise Example:**
**Klarna Customer Service**: Klarna's AI agent doesn't just tell users "You can check your invoice in the app." It has access to tools that can actually pull up the invoice details, extend a payment due date, or initiate a refund process directly within the chat, resolving the user's problem end-to-end without human intervention.
