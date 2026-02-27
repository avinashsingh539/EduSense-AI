# modules/ui_renderer.py

import streamlit as st
import re


def render_study_material(text: str):
    if not text or len(text.strip()) < 50:
        st.warning("⚠️ No study material to display.")
        return

    # Split sections by markdown headings
    sections = re.split(r"\n###\s+", text)

    for section in sections:
        if not section.strip():
            continue

        lines = section.strip().split("\n")
        title = lines[0]
        content = "\n".join(lines[1:]).strip()

        # ---------- NOTES ----------
        if "Structured Study Notes" in title:
            st.markdown("## 📘 Structured Study Notes")
            st.markdown(content)

        # ---------- KEY CONCEPTS ----------
        elif "Key Concepts" in title:
            st.markdown("## 🔑 Key Concepts")
            st.markdown(content)

        # ---------- FLASHCARDS ----------
        elif "Flashcards" in title:
            st.markdown("## 🧠 Flashcards")
            cards = content.split("\n\n")
            for card in cards:
                if card.strip():
                    with st.expander("📌 Flashcard"):
                        st.markdown(card)

        # ---------- MCQs ----------
        elif "MCQs" in title:
            st.markdown("## 📝 MCQs")
            questions = content.split("\n\n")
            for q in questions:
                if q.strip():
                    with st.expander("❓ Question"):
                        st.markdown(q)

        # ---------- EXPLANATION ----------
        elif "Explanation" in title:
            st.markdown("## 👶 Beginner-Friendly Explanation")
            st.markdown(content)

        # ---------- FALLBACK ----------
        else:
            st.markdown(f"## {title}")
            st.markdown(content)