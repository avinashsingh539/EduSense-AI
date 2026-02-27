import streamlit as st
from fpdf import FPDF

def download_markdown(text, filename="output.md"):
    st.download_button(
        label="📄 Download as Markdown",
        data=text,
        file_name=filename,
        mime="text/markdown"
    )

def download_pdf(text, filename="output.pdf"):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    pdf_bytes = pdf.output(dest="S").encode("latin-1")

    st.download_button(
        label="📕 Download as PDF",
        data=pdf_bytes,
        file_name=filename,
        mime="application/pdf"
    )