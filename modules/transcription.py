# modules/transcription.py

import whisper
import os
import subprocess
import uuid

# ---------------- LOAD MODEL ONCE ----------------
model = whisper.load_model("small")


# ---------------- AUDIO EXTRACTION ----------------
def extract_audio_from_video(video_path: str) -> str:
    """
    Extracts clean, normalized mono audio from video.
    """
    audio_path = f"temp_audio_{uuid.uuid4().hex}.wav"

    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",                  # mono
        "-ar", "16000",               # 16kHz
        "-sample_fmt", "s16",         # 16-bit PCM
        "-af", "highpass=f=80,lowpass=f=8000,afftdn,loudnorm",
        audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return audio_path


# ---------------- SILENCE-BASED SPLITTER ----------------


def split_audio_fixed(audio_path: str, segment_sec=30) -> list:
    import subprocess, os

    output_pattern = "audio_chunk_%03d.wav"

    subprocess.run([
        "ffmpeg", "-y",
        "-i", audio_path,
        "-f", "segment",
        "-segment_time", str(segment_sec),
        "-reset_timestamps", "1",
        output_pattern
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    chunks = sorted([
        f for f in os.listdir()
        if f.startswith("audio_chunk_") and f.endswith(".wav")
    ])

    return chunks

# ---------------- TRANSCRIBE AUDIO ----------------
def transcribe_audio(audio_path: str) -> str:
    full_text = []

    audio_chunks = split_audio_fixed(audio_path)

    if not audio_chunks:
        audio_chunks = [audio_path]

    for chunk in audio_chunks:
        try:
            # Skip tiny chunks
            if os.path.getsize(chunk) < 50_000:
                continue

            result = model.transcribe(
                chunk,
                language="en",
                fp16=False,
                temperature=0.0,
                condition_on_previous_text=True,
                no_speech_threshold=0.4,
                compression_ratio_threshold=2.4,
                initial_prompt=(
                    "This is a continuous English lecture. "
                    "Transcribe all spoken content accurately."
                )
            )

            text = result.get("text", "").strip()
            if text:
                full_text.append(text)

        except RuntimeError as e:
            print(f"[WARN] Skipping chunk {chunk}: {e}")

        finally:
            if chunk != audio_path and os.path.exists(chunk):
                os.remove(chunk)

    return " ".join(full_text)

def polish_transcript(text: str) -> str:
    """
    Light grammar + spelling correction.
    No summarization.
    """
    prompt = f"""
Fix grammar, spelling, and punctuation in the following transcript.
Do NOT change meaning.
Do NOT summarize.
Keep original wording as much as possible.

Transcript:
{text}
"""
    response = model.generate_content(prompt)
    return response.text


# ---------------- TRANSCRIBE VIDEO ----------------
def transcribe_video(video_path: str) -> str:
    """
    Full video → clean audio → silence-aware transcription.
    """
    audio_path = extract_audio_from_video(video_path)
    text = transcribe_audio(audio_path)

    if os.path.exists(audio_path):
        os.remove(audio_path)

    return text