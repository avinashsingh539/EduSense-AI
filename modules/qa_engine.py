def answer_question(question: str, lecture_text: str) -> str:
    if not question or not lecture_text:
        return "Please provide a valid question."

    # Simple fallback (no API)
    return (
        "📌 Question:\n"
        f"{question}\n\n"
        "📖 Answer (based on lecture content):\n"
        f"{lecture_text[:600]}...\n\n"
        "(Note: Gemini API disabled)"
    )