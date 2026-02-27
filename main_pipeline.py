from modules.transcription import transcribe_video
from modules.text_cleaner import clean_text
from modules.chunk_processor import split_text
from modules.learning_engine import generate_study_material


# Put a small test video in project root
video_path = "sample.mp4"

print("🎙 Transcribing video...")
text = transcribe_video(video_path)

print("🧹 Cleaning transcript...")
cleaned = clean_text(text)

print("✂ Splitting into chunks...")
chunks = split_text(cleaned)

print(f"📦 Total chunks: {len(chunks)}")

all_outputs = []

for idx, chunk in enumerate(chunks, start=1):
    print(f"🧠 Processing chunk {idx}/{len(chunks)}")
    summary = generate_study_material(chunk)
    all_outputs.append(summary)

final_output = "\n\n".join(all_outputs)

print("\n===== FINAL OUTPUT =====\n")
print(final_output)