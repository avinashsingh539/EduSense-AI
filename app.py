import streamlit as st
import os
import time

from modules.ui_renderer import render_study_material
from modules.transcription import transcribe_audio, transcribe_video
from modules.youtube_processor import download_audio_from_youtube
from modules.text_cleaner import clean_text
from modules.chunk_processor import split_text
from modules.export_utils import download_markdown, download_pdf
from modules.qa_engine import answer_question
from modules.learning_engine import (
    generate_mini_summary,
    generate_study_material
)

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EduSense AI",
    layout="centered"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- BLINKING INFO CSS ----------------
st.markdown(
    """
    <style>
    @keyframes blink {
        0% {opacity: 1;}
        50% {opacity: 0.2;}
        100% {opacity: 1;}
    }
    .blink-box {
        animation: blink 1.5s linear infinite;
        background-color: #fff3cd;
        color: #856404;
        padding: 16px;
        border-radius: 10px;
        border: 1px solid #ffeeba;
        font-size: 16px;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 EduSense AI – Lecture Intelligence System")
st.caption("Turn lectures into structured study material")

# ---------------- FIRST-TIME USER NOTICE ----------------
if "seen_notice" not in st.session_state:
    st.markdown(
        """
        <div class="blink-box">
        ⚠️ <b>Important Instructions</b><br><br>
        • Upload <b>English language</b> audio/video only<br>
        • Supported: <b>Audio, Video, YouTube URL</b><br>
        • <b>Cloud demo:</b> Max <b>2–3 minutes</b><br>
        • Longer lectures supported locally
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- INPUT SELECTION ----------------
input_type = st.radio(
    "Select Input Type:",
    ["Upload Audio", "Upload Video", "YouTube URL"]
)

text = None
file_path = None
MAX_FILE_SIZE_MB = 20  # Cloud demo limit

def file_size_in_mb(file):
    return len(file.getvalue()) / (1024 * 1024)

# ---------------- AUDIO ----------------
if input_type == "Upload Audio":
    uploaded_file = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
    if uploaded_file:
        if file_size_in_mb(uploaded_file) > MAX_FILE_SIZE_MB:
            st.error("Cloud demo supports only 2–3 minutes.")
            st.stop()

        file_path = "temp_audio.wav"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("🎙 Transcribing audio..."):
            st.session_state["seen_notice"] = True
            text = transcribe_audio(file_path)

# ---------------- VIDEO ----------------
elif input_type == "Upload Video":
    uploaded_file = st.file_uploader("Upload Video File", type=["mp4"])
    if uploaded_file:
        if file_size_in_mb(uploaded_file) > MAX_FILE_SIZE_MB:
            st.error("Cloud demo supports only 2–3 minutes.")
            st.stop()

        file_path = "temp_video.mp4"
        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        with st.spinner("🎬 Transcribing video..."):
            st.session_state["seen_notice"] = True
            text = transcribe_video(file_path)

# ---------------- YOUTUBE ----------------
elif input_type == "YouTube URL":
    url = st.text_input("Enter YouTube URL")
    if url:
        with st.spinner("⬇ Downloading audio from YouTube..."):
            file_path = download_audio_from_youtube(url)

        with st.spinner("🎙 Transcribing YouTube audio..."):
            st.session_state["seen_notice"] = True
            text = transcribe_audio(file_path)

# ---------------- PROCESS PIPELINE ----------------
if text:
    with st.spinner("🧹 Cleaning transcript..."):
        cleaned = clean_text(text)

    with st.spinner("✂ Splitting into chunks..."):
        chunks = split_text(cleaned)

    st.info(f"📦 Lecture split into {len(chunks)} chunk(s)")

    # -------- STAGE 1: MINI SUMMARIES --------
    mini_summaries = []
    with st.spinner("🧠 Creating mini summaries..."):
        for idx, chunk in enumerate(chunks, start=1):
            st.caption(f"Summarizing chunk {idx}/{len(chunks)}")
            mini = generate_mini_summary(chunk)
            if mini:
                mini_summaries.append(mini)
            time.sleep(0.2)

    combined_summary = " ".join(mini_summaries)

    # -------- STAGE 2: FINAL OUTPUT --------
    with st.spinner("📘 Generating final study material..."):
        final_output = generate_study_material(combined_summary)

    st.session_state["final_output"] = final_output
    st.session_state["lecture_summary"] = combined_summary

    st.success("✅ Study material generated successfully")

    st.divider()
    render_study_material(final_output)
    st.divider()

    # -------- DOWNLOAD SECTION (FIXED) --------
    st.subheader("⬇ Download Study Material")

    col1, col2 = st.columns(2)

    with col1:
        download_markdown(
            final_output,
            filename="EduSense_Study_Material.md"
        )

    with col2:
        download_pdf(
            final_output,
            filename="EduSense_Study_Material.pdf"
        )

# ---------------- Q&A SECTION ----------------
st.divider()
st.subheader("💬 Ask Questions from Lecture")

question = st.text_input("Ask a question based on the lecture:")

if question:
    with st.spinner("🤔 Thinking..."):
        answer = answer_question(
            question,
            st.session_state.get("lecture_summary", "")
        )
    st.markdown(answer)

# ---------------- CLEANUP ----------------
if file_path and os.path.exists(file_path):
    os.remove(file_path)