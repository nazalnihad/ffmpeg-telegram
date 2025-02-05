from pytubefix import YouTube
from pytubefix.cli import on_progress

url = input("Enter link here : ")

yt = YouTube(url, on_progress_callback=on_progress)
print("Video Title:", yt.title)

res = input("Enter resolution here (e.g. 720p): ")

# Get stream with both video and audio
streams = yt.streams.filter(resolution=res, progressive=True).first()

if streams:
    print(f"Downloading: {yt.title} in {res} resolution")
    streams.download()
    print("Download completed!")
else:
    print("No matching stream found. Try a different resolution.")
