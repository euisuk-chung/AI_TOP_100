# Question
Agents repeat the same wrong answer every time.

# Answer
Reflection

# Explanation
**The Problem:**
Insanity is doing the same thing over and over and expecting different results. Simple agents are stateless; if they fail to solve a math problem once, they will likely fail the exact same way the second time because they don't "know" they failed.

**The Solution: Reflection**
Reflection adds a "Self-Review" step.
1. **Attempt**: Agent tries to solve the problem.
2. **Critique**: Agent (or a separate prompt) looks at the result: "Wait, the answer is negative, but it should be positive."
3. **Retry**: Agent tries again, explicitly instructed to fix the error found in step 2.

It turns a "dumb" loop into a "learning" loop.

**Real Enterprise Example:**
**Writer (Enterprise AI Platform)**: Writer uses reflection in its content generation workflows. If a user asks for a blog post that must follow specific brand guidelines (e.g., "No passive voice"), the agent generates a draft, then a "Reflector" step checks the draft against the guidelines. If it finds passive voice, it instructs the generator to rewrite those specific sentences before showing the final result to the user.
