# Question
Agents produce correct outputs but have no sense of preference.

# Answer
Critic

# Explanation
**The Problem:**
If you ask an agent to "Write a poem," it will write one. But is it *good*? Is it *better* than the last one? A standard agent just aims to complete the task, not necessarily to optimize for quality or specific stylistic preferences.

**The Solution: Critic**
A Critic is a separate role or model that judges the output.
- **Evaluation**: "This poem rhymes, but the meter is off."
- **Feedback**: It gives specific feedback to the generator.
- **Iterative Improvement**: The generator uses this feedback to write a better version.

It separates the "doing" from the "judging," leading to higher quality results.

**Real Enterprise Example:**
**Automated Code Review Systems**: In software development, a "Coder Agent" might generate a function to solve a problem. A separate "Critic Agent" (acting as a Senior Engineer) reviews the code for security vulnerabilities, style guide violations, and efficiency. It rejects the code if it uses an insecure library, forcing the Coder Agent to rewrite it before a human ever sees it.
