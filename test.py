import os
import re
from pytubefix import YouTube
from pytubefix.cli import on_progress

def get_download_dir():
    """Set default download directory in Termux."""
    download_dir = "downloads"
    os.makedirs(download_dir, exist_ok=True)
    return download_dir

def validate_youtube_url(url):
    """Validate YouTube URL."""
    youtube_regex = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+'
    return bool(re.match(youtube_regex, url))

def get_youtube_streams(url):
    """Fetch available MP4 streams."""
    if not validate_youtube_url(url):
        print("Invalid YouTube URL.")
        return None, None
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        print(f"\nTitle: {yt.title}")
        streams = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc()
        if not streams:
            print("No MP4 streams available.")
            return None, None
        return yt, streams
    except Exception as e:
        print(f"Error fetching video: {e}")
        return None, None

def display_streams(streams):
    """Display available streams."""
    print("\nAvailable Resolutions:")
    for i, stream in enumerate(streams):
        resolution = stream.resolution or "Unknown"
        size_mb = stream.filesize_mb if stream.filesize_mb else "N/A"
        print(f"{i+1}. {resolution}, {stream.mime_type}, {size_mb:.2f} MB")

def sanitize_filename(filename):
    """Sanitize filename for safe saving."""
    return re.sub(r'[^\w\s.-]', '', filename).replace(' ', '_')

def download_stream(yt, streams, choice, output_dir):
    """Download selected stream."""
    if not (0 <= choice < len(streams)):
        print("Invalid selection.")
        return None
    try:
        stream = streams[choice]
        print(f"\nDownloading: {yt.title} ({stream.resolution or 'Unknown'})")
        filename = f"{sanitize_filename(yt.title)}_{stream.resolution or 'unknown'}.mp4"
        output_path = os.path.join(output_dir, filename)
        if os.path.exists(output_path):
            print(f"File {filename} already exists.")
            return output_path
        stream.download(output_path=output_dir, filename=filename)
        print(f"Saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error downloading: {e}")
        return None

def main():
    output_dir = get_download_dir()
    url = input("Enter YouTube link: ").strip()
    if not url:
        print("No URL provided.")
        return
    yt, streams = get_youtube_streams(url)
    if not yt or not streams:
        return
    display_streams(streams)
    try:
        choice = int(input("\nSelect stream number (0 to cancel): ")) - 1
        if choice == -1:
            print("Cancelled.")
            return
    except ValueError:
        print("Invalid input.")
        return
    download_stream(yt, streams, choice, output_dir)

if __name__ == "__main__":
    main()