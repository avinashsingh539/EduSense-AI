from pytubefix import YouTube


def download_audio_from_youtube(url: str) -> str:
    yt = YouTube(url)

    stream = yt.streams.filter(only_audio=True).first()

    output_file = stream.download(filename="yt_audio.mp4")
    return output_file