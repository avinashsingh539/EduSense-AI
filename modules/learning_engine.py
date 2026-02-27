# modules/learning_engine.py

import os

# ==================================================
# CONFIG

# ==================================================
USE_GEMINI = True  # 🔁 Flip to True when quota is available

# Try loading Gemini SDK (newer one)
try:
    from google import genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

# Initialize client only if enabled
if USE_GEMINI and GEMINI_AVAILABLE:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
else:
    client = None


# ==================================================
# STAGE 1 — MINI SUMMARY (Hierarchical Compression)
# ==================================================
def generate_mini_summary(text: str) -> str:
    """
    Compress a chunk into a short semantic summary.
    No structure, no Q&A, no MCQs.
    """

    if not text or len(text.strip()) < 80:
        return ""

    # Fallback mode (NO API)
    if not USE_GEMINI or client is None:
        cleaned = text.replace("\n", " ").strip()
        return cleaned[:300] + "..."

    prompt = f"""
Summarize the following lecture section clearly and concisely.
Focus only on key ideas, definitions, and explanations.
Do NOT create flashcards, MCQs, or structured notes.

Lecture Section:
{text}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print("[WARN] Mini summary failed:", e)
        return ""


# ==================================================
# STAGE 2 — FINAL STRUCTURED OUTPUT
# ==================================================
def generate_study_material(text: str) -> str:
    """
    Generate final structured academic output
    from merged mini-summaries.
    """

    if not text or len(text.strip()) < 100:
        return "⚠️ Not enough content to generate study material."

    # Fallback mode (NO API)
    if not USE_GEMINI or client is None:
        return f"""
📘 STUDY NOTES (AUTO-GENERATED)

Summary:
{text[:600]}...

Key Concepts:
- Core ideas extracted from lecture

Flashcards:
Q: What is the lecture mainly about?
A: Derived from summarized content

MCQs:
1. What best describes the lecture?
A) Overview
B) Explanation
C) Example
D) Conclusion
Answer: B

(Simple mode – API disabled)
"""

    prompt = f"""
You are an academic lecture analyzer.

From the following condensed lecture summary, generate:

1. Structured Study Notes
   - Organized with headings
   - Logical flow
   - No repetition

2. Key Concepts (bullet list)

3. 5 Flashcards (Q&A format)

4. 5 MCQs
   - 4 options each
   - Correct answer clearly marked

5. Beginner-friendly explanation of the full topic

Do NOT repeat content.
Ensure coherence across all sections.

Lecture Summary:
{text}
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-flash-latest",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ Generation failed: {str(e)}"