# EduSense AI – Lecture Voice-to-Notes Generator

EduSense AI is an AI-powered lecture intelligence system that converts spoken lectures into structured study material such as notes, flashcards, quizzes, and simplified explanations.

The system is designed to help students focus on understanding lectures instead of worrying about note-taking.

---

## 🚨 Problem Statement

Students often miss key concepts during lectures because listening, understanding, and writing notes simultaneously is difficult.  
Recorded lectures are long and unstructured, making revision time-consuming and inefficient.

A system is required that can:
- Convert lecture speech into text
- Remove noise and filler words
- Organize content into structured study material
- Support revision through quizzes and flashcards

---

## 💡 Solution Overview

EduSense AI processes lecture **audio, video, or YouTube links** using speech-to-text AI and generative AI to automatically produce:

- Structured study notes
- Key concepts
- Flashcards
- Multiple-choice questions (MCQs)
- Beginner-friendly explanations

The project supports:
- **Local execution** for longer lectures
- **Cloud demo (Streamlit free tier)** for short lecture previews

---

## 🏗️ System Architecture

**Pipeline Flow:**

Input Source  
→ Speech-to-Text (Whisper)  
→ Text Cleaning  
→ Chunk Processing  
→ Hierarchical Summarization  
→ Structured Content Generation  
→ Streamlit User Interface

**Key Design Choice:**  
Hierarchical summarization is used to avoid repetition and improve coherence for long lectures.

---

## ⚙️ Technologies Used

- **Python** – Core programming language
- **OpenAI Whisper** – Speech-to-text transcription
- **Google Gemini API** – Generative AI for notes, quizzes, and explanations
- **Streamlit** – Web-based frontend
- **FFmpeg** – Audio extraction and processing
- **GitHub** – Version control and collaboration

---

## 🚀 Key Features

- 🎧 Supports **Audio, Video, and YouTube URLs**
- 🧠 Hierarchical summarization for long lectures
- 📘 Structured academic notes generation
- 🧠 Flashcards for quick revision
- 📝 MCQs for self-assessment
- 👶 Beginner-friendly explanations
- 📄 Download notes as **Markdown or PDF**
- 💬 Ask questions from the lecture content
- ☁️ Cloud demo + full local version

---

## 🖥️ User Interface Walkthrough (After Running the App)

Once the application is launched using Streamlit, the user experiences the following flow:

### 🔹 1. Home Screen
- Displays the project title **“EduSense AI – Lecture Intelligence System”**
- Shows a blinking instruction box informing users:
  - Only English lectures are supported
  - Audio, Video, and YouTube inputs are accepted
  - Cloud demo supports short lectures (2–3 minutes)

---

### 🔹 2. Input Selection
Users can choose one of the following input types:
- **Upload Audio** (MP3 / WAV)
- **Upload Video** (MP4)
- **YouTube URL**

Each input option dynamically updates the interface.

---

### 🔹 3. File / URL Upload
- Users upload a file or paste a YouTube link
- The system validates file size (for cloud demo)
- Clear error messages are shown if limits are exceeded

---

### 🔹 4. Transcription Phase
- A progress spinner indicates transcription is in progress
- Audio is cleaned and processed automatically
- Users do not need to perform any manual preprocessing

---

### 🔹 5. Processing & Summarization
The system performs:
- Transcript cleaning
- Chunk splitting
- Mini summaries for each chunk
- Final structured academic generation

A progress indicator shows the current processing stage.

---

### 🔹 6. Generated Output Display
The final output is rendered in a **clean, readable, and professional layout**, including:
- 📘 Structured Study Notes
- 🔑 Key Concepts
- 🧠 Flashcards (expandable)
- 📝 MCQs (with correct answers)
- 👶 Beginner-friendly explanation

Each section is clearly separated for easy reading.

---

### 🔹 7. Download Options
Users can download the generated study material as:
- 📄 Markdown file
- 📄 PDF document

This allows offline study and sharing.

---

### 🔹 8. Ask Questions from Lecture
Users can type natural-language questions related to the lecture, such as:
- “What is the main concept explained?”
- “Summarize the first topic”
- “Explain this topic in simple terms”

The system responds using the lecture context.

---

## ☁️ Cloud Demo Limitations (Important)

Due to Streamlit free-tier constraints:
- Audio/Video length is limited to **2–3 minutes**
- English language only
- YouTube transcription may be unstable due to platform restrictions

👉 **Local execution is recommended for full functionality.**

---

## 🖥️ Local Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/avinashsingh539/EduSense-AI.git
cd EduSense-AI

### 2️⃣ Create Virtual Environment

python -m venv venv
venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Set API Key

Create an environment
### 4️⃣ Set API Key
setx GEMINI_API_KEY "YOUR_API_KEY"

### 5️⃣ Run App
streamlit run app.py

📦 Deployment

The application is deployed on Streamlit Cloud (free tier).

🔗 Live Demo Link: https://edusense-ai-hrwjzesimc2t8gdggojgum.streamlit.app/
🔗 GitHub Repository: https://github.com/avinashsingh539/EduSense-AI/

🔮 Future Enhancements

Multi-language support

Speaker detection

Timestamped notes

Scalable cloud deployment



