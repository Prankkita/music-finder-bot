from utils.download_reel import download_reel

if __name__ == "__main__":
    reel_url = input("Enter the Instagram reel URL: ")
    try:
        video_path = download_reel(reel_url)
        print(f"Downloaded Video successfully: {video_path}")
    except Exception as e:
        print(f"Failed to download video: {e}")
        