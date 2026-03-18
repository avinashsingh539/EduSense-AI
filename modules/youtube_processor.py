import subprocess
import uuid
import os

def download_audio_from_youtube(url: str) -> str:
    output_file = f"yt_audio_{uuid.uuid4().hex}.mp3"

    command = [
        "yt-dlp",
        "-x",                        # extract audio
        "--audio-format", "mp3",
        "-o", output_file,
        url
    ]

    try:
        subprocess.run(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
    except subprocess.CalledProcessError:
        raise RuntimeError("❌ Failed to download YouTube audio. Try another video.")

    if not os.path.exists(output_file):
        raise RuntimeError("❌ Audio file not created.")

    return output_file