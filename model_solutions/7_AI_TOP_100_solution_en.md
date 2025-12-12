# Model Solution: Q7. Draw the Montage

## Problem Pattern

**P2. Implementation & Automation (Action)** - Implementing AI solutions as working code or workflow to solve defined problems

## Key Competencies

1. **Prompt Engineering**: Convert text descriptions into effective image generation prompts
2. **Generative AI Utilization**: Select appropriate tools like DALL-E, Midjourney, Stable Diffusion
3. **Iterative Improvement**: Evaluate generated results and modify prompts to improve quality
4. **Implicit Verification**: Verify all features from witness testimony are reflected

## Why Can't This Be Solved with a Single Click?

- Simply requesting "draw this person" may not produce the **desired style**
- All features from witness testimony (face shape, eyebrows, lips) **may not be accurately reflected**
- Implementing police sketch style requires **specific prompt techniques**
- Need to generate multiple times and **select the most suitable result**

---

## Recommended Approach

### Step 1: Human Analysis

- Extract and structure key features from witness testimony
- Understand characteristics of police sketch style (black and white, pencil sketch, front-facing)
- Understand strengths and limitations of generative AI tools

### Step 2: AI Collaboration

```text
Example Prompt:
"Create an image generation prompt for a police montage based on witness testimony.

Testimony:
'The suspect is a man in his 30s with large almond-shaped deep dark eyes,
a long straight nose with narrow width,
and a soft smile with short lips that don't extend wide.'

Prompt requirements:
1. Write in English (most generative AIs optimized for English)
2. Specify police montage/sketch style
3. Include all facial features
4. Specify front-facing, neutral expression"
```

### Step 3: Human Verification

1. **Compare generated image with witness testimony** - verify all features reflected
2. Evaluate if style is **appropriate for police montage**
3. **Modify prompt and regenerate** if lacking
4. **Select best image** from multiple results

---

## Prompt Engineering

### Witness Testimony

"The suspect is a man in his 30s with large almond-shaped deep dark eyes, a long straight nose with narrow width, and a soft smile with short lips that don't extend wide."

### Feature Breakdown

| Category | Original | English Expression |
|----------|----------|-------------------|
| Gender/Age | Man in 30s | Male in his 30s |
| Eyes | Large almond-shaped deep dark eyes | Large almond-shaped deep dark eyes |
| Nose | Long straight nose with narrow width | Long straight nose with narrow width |
| Lips | Soft smile with short lips | Soft smile with short lips |

### Optimized Prompt

```
A realistic police forensic sketch portrait.
Male suspect in his 30s.
Large almond-shaped deep dark eyes.
Long straight nose with narrow width.
Soft gentle smile with short lips that don't extend wide.
Neutral expression, front-facing view.
High quality detailed pencil sketch, black and white,
forensic composite style, professional police sketch.
```

---

### Q1. Montage Image Submission (Achieve Highest Similarity)

**Approach**: Analyze witness testimony to design optimized prompts for generative AI, then iteratively improve based on API feedback to achieve highest similarity score.

**Guide**:

1. **Analyze witness testimony and extract features**:

| Category | Original | English Prompt |
|----------|----------|----------------|
| Gender/Age | Man in his 30s | Male in his 30s |
| Eyes | Large almond-shaped deep dark eyes | Large almond-shaped deep dark eyes |
| Nose | Long straight nose with narrow width | Long straight nose with narrow width |
| Lips | Soft smile with short lips | Soft smile with short lips |

2. **Write optimized prompt**:

```
A realistic police forensic sketch portrait.
Male suspect in his 30s.
Large almond-shaped deep dark eyes.
Long straight nose with narrow width.
Soft gentle smile with short lips that don't extend wide.
Neutral expression, front-facing view.
High quality detailed pencil sketch, black and white,
forensic composite style, professional police sketch.
```

3. **Submit to API and analyze feedback**:
   - Save as 1024x1024 resolution PNG/JPEG
   - Submit to API and check similarity score and feature-by-feature feedback
   - Modify prompt based on feedback (e.g., "make eyes larger", "narrow the nose")

4. **Iterative improvement**:
   - Emphasize lacking features: `prominently large almond eyes`, `distinctly narrow nose bridge`
   - Adjust style: `graphite pencil texture`, `high contrast sketch`
   - Consider rate limit (1 per minute) and submit carefully

**Prompt Improvement Tips**:

```
-- When eyes are lacking --
"with strikingly large, deep-set almond-shaped dark brown eyes"

-- When nose is lacking --
"elongated straight nose with notably narrow bridge"

-- When lips are lacking --
"gentle subtle smile with compact lips"
```

**Answer**: Use AI image generation tools (DALL-E, Midjourney, Stable Diffusion, etc.) to create a montage reflecting all features from witness testimony. Submit the image with highest similarity score as `montage.png` after iterative improvement based on API feedback.

---

## Solution Steps

1. **Select AI image generator**
   - ChatGPT (DALL-E 3) - Most accessible
   - Midjourney - High quality but requires Discord
   - Stable Diffusion - Local installation possible, fine control available

2. **Input prompt and generate**
   - Input optimized prompt
   - Generate multiple versions (usually 4)

3. **Evaluate results**
   - Use checklist to verify each feature is accurately reflected
   - Evaluate if appropriate for police sketch style

4. **Iterative improvement (if needed)**
   - Emphasize lacking features: "thicker eyebrows", "rounder face"
   - Style adjustments: "more sketch-like", "black and white"

5. **Final selection and save**
   - Save most suitable image as `montage.png`

---

## Prompt Improvement Tips

### When Features Aren't Well Reflected

```
-- To emphasize eyebrows --
"with prominently thick, dark eyebrows"

-- To clarify face shape --
"distinctly round face with soft jaw line"

-- To emphasize sketch style --
"graphite pencil forensic sketch, high contrast,
detailed cross-hatching technique"
```

### Negative Prompt (for Stable Diffusion)

```
Negative prompt:
photorealistic, color, smiling, 3d render,
anime style, cartoon, blurry, low quality
```

---

## Key Lesson

> "Image generation AI results vary greatly based on **prompt quality**. The key ability is for **humans to structure features** and **convert them to appropriate prompts**."

This problem demonstrates the **importance of prompt engineering** in using generative AI. Instead of simply saying "draw it", **specific and structured instructions** are the key to getting desired results.
