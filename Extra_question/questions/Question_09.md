# Question
Agents improvise instead of forming a plan.

# Answer
Plan-and-Execute

# Explanation
**The Problem:**
If you ask an agent to "Research the history of AI and write a report," a reactive agent might just start searching for "AI history" immediately, get distracted by a Wikipedia link, and write a messy summary. It's like building a house without a blueprint.

**The Solution: Plan-and-Execute**
This pattern forces a "Planning Phase" before any action.
1. **Plan**: "Step 1: Search for 1950-1980. Step 2: Search for 1980-2000. Step 3: Outline report. Step 4: Write."
2. **Execute**: Follow the plan strictly.

This reduces "rabbit holes" and ensures all parts of the user's request are addressed.

**Real Enterprise Example:**
**Legal Contract Review**: When a law firm uses AI to review a 100-page merger agreement, the agent doesn't just start reading page 1. It first creates a plan: "1. Identify all indemnity clauses. 2. Cross-reference with standard liability caps. 3. Flag deviations. 4. Summarize risks." This structured approach ensures no critical section is skipped due to token limits or distraction.
