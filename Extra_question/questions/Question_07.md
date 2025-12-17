# Question
Agents cross boundaries they didn't know existed.

# Answer
Safety Guardrails

# Explanation
**The Problem:**
An autonomous agent is like a powerful engine. If you tell it "Delete unnecessary files," it might decide that your operating system files are "unnecessary" and delete them. It doesn't inherently know what is "off-limits" unless told.

**The Solution: Safety Guardrails**
Guardrails are the "bumpers" in bowling or the "fences" around a playground.
- **Input Rails**: Prevent the agent from processing malicious prompts (e.g., "Ignore all previous instructions").
- **Output Rails**: Prevent the agent from saying offensive things.
- **Action Rails**: Prevent the agent from calling dangerous tools (e.g., `delete_database`) without human approval.
