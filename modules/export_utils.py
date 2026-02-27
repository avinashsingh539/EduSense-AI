# modules/export_utils.py

import streamlit as st
from fpdf import FPDF
import re


def _sanitize_text(text: str) -> str:
    """
    Converts Unicode characters to PDF-safe ASCII.
    """
    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "•": "-",
        "🔑": "",
        "📘": "",
        "🧠": "",
        "👶": "",
        "⬇": "",
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    # Remove any remaining non-latin characters
    text = re.sub(r"[^\x00-\xFF]", "", text)
    return text


def download_markdown(text, filename="EduSense_Study_Material.md"):
    st.download_button(
        label="📄 Download as Markdown",
        data=text,
        file_name=filename,
        mime="text/markdown"
    )


def download_pdf(text, filename="EduSense_Study_Material.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    safe_text = _sanitize_text(text)

    for line in safe_text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf_bytes = pdf.output(dest="S").encode("latin-1", errors="ignore")

    st.download_button(
        label="📕 Download as PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf"
    )