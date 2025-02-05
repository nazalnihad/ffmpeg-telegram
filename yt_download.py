from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_vid(link,resolution):
    url = link
    res = resolution
    yt = YouTube(url, on_progress_callback=on_progress)
    print("Video Title:", yt.title)

    #stream with both video and audio
    streams = yt.streams.filter(resolution=res, progressive=True).first()

    if streams:
        print(f"Downloading: {yt.title} in {res} resolution")
        streams.download(output_path="downloads/")
        print("Download completed!")
    else:
        print("No matching stream found. Try a different resolution.")

download_vid("link","360p")