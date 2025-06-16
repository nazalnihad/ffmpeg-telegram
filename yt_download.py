from pytubefix import YouTube
from pytubefix.cli import on_progress

url = input("Enter link here: ")
yt = YouTube(url, on_progress_callback=on_progress)
print("Video Title:", yt.title)

# Display all available streams
print("\nAvailable streams:")
for i, stream in enumerate(yt.streams.filter(progressive=True)):
    print(f"{i+1}. Resolution: {stream.resolution}, Format: {stream.mime_type}, Size: {stream.filesize_mb:.2f} MB")

# Let user choose a stream
choice = int(input("\nEnter the number of the stream you want to download: ")) - 1

if 0 <= choice < len(yt.streams.filter(progressive=True)):
    selected_stream = yt.streams.filter(progressive=True)[choice]
    print(f"\nDownloading: {yt.title}")
    print(f"Resolution: {selected_stream.resolution}, Format: {selected_stream.mime_type}")
    selected_stream.download()
    print("Download completed!")
else:
    print("Invalid selection. Please run the script again.")
