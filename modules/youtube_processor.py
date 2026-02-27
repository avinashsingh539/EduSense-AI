# modules/youtube_processor.py

from pytube import YouTube
import os

def download_audio_from_youtube(url: str) -> str:
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()

    output_path = audio_stream.download(filename="yt_audio")
    
    # Convert to .wav for Whisper
    base, _ = os.path.splitext(output_path)
    audio_path = base + ".wav"

    os.rename(output_path, audio_path)
    return audio_path
