# Model Solution: Q2. Secret of Ancient Ruins

## Problem Pattern

**P2. Implementation & Automation (Action)** - Implementing AI solutions as working code or workflow to solve defined problems

## Key Competencies

1. **Image Code Extraction**: Use AI's OCR/vision to accurately extract obfuscated code from images
2. **Code Interpretation & Execution**: Analyze obfuscated C code and verify by actual execution
3. **Human-in-the-loop Verification**: Human directly compiles/runs to verify AI-extracted code accuracy

## Why Can't This Be Solved with a Single Click?

- Code in image is **obfuscated** making accurate AI recognition difficult
- Minor character errors (e.g., `0` vs `O`, `1` vs `l`) significantly affect results
- **Must run the code** to confirm the answer (AI inference alone is inaccurate)

---

## Recommended Approach

### Step 1: Human Analysis

- Identify hints from the problem: `main.c`, `gcc -w` keywords
- Understand rough structure of code in image (variable names, function structure)

### Step 2: AI Collaboration

```text
Example Prompt:
"Extract the C code exactly from this image.
Since it's obfuscated code, carefully distinguish special characters, numbers, and letters.
Pay special attention to differentiating 0 and O, 1 and l."
```

### Step 3: Human Verification

1. Save AI-extracted code as `main.c`
2. Compile with `gcc -w main.c -o main`
3. If compilation error → share error message with AI and request fix
4. Run `./main` and test with input values
5. Verify results and submit answer

---

### Q1. Programming Language Identification

**Approach**: Analyze hints from the problem (`main.c`, `gcc`) and code syntax to identify the programming language.

**Guide**:

1. Check filename `main.c` and compiler `gcc` in problem description
2. Confirm C language features in image code: `#include <stdio.h>`, `void`, `char*`, `printf`
3. Eliminate other language possibilities

**Analysis Results**:

| Hint | Evidence |
|------|----------|
| main.c | C language source file extension |
| gcc | GNU C Compiler |
| #include <stdio.h> | C standard library header |

**Answer**: **2. C**

---

### Q2. Output for Input `1q2w3e4r`

**Approach**: Extract code from image, compile, and run to check output.

**Guide**:

1. Use AI to extract C code from image
2. Save extracted code as `main.c`
3. Compile: `gcc -w main.c -o main`
4. Run: `./main`
5. Input: `1q2w3e4r`
6. Check output result

**Code Execution Process**:

```bash
$ gcc -w main.c -o main
$ ./main
1q2w3e4r
RWETQSDR
```

**Cautions**:

- AI-extracted code may have OCR errors
- If compilation error occurs, share error message with AI and request fix
- Watch for confusion between `0` and `O`, `1` and `l`, `5` and `S`

**Answer**: **RWETQSDR**

---

### Q3. Output for Input `STOP`

**Approach**: Same process as Q2, only changing input to `STOP`.

**Guide**:

1. Use executable compiled in Q2
2. Run: `./main`
3. Input: `STOP`
4. Check output result

**Code Execution Process**:

```bash
$ ./main
STOP
KAKAO2025
```

**Hint Interpretation**: "Only when you stop can you see"

- Input `STOP` connects to the problem's riddle
- Code is designed to output hidden message for specific input (`STOP`)

**Answer**: **KAKAO2025**

---

## Key Lesson

> "AI can extract code from images, but whether the result is accurate can only be known by **actually running it**."

This problem shows the core of Human-in-the-loop: utilizing AI's vision and code analysis capabilities while **human performs final verification**.
