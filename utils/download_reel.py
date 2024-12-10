import instaloader
import os

def download_reel(reel_url):
    """Download an Instagram reel using the provided URL."""
    loader = instaloader.Instaloader(dirname_pattern="downloads", filename_pattern="{shortcode}")
    try:
        # Extract the shortcode from the URL
        shortcode = reel_url.split("/")[-2]

        # Load the post using shortcode
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Download the post
        loader.download_post(post, target="downloads")

        print("Reel downloaded successfully.")

        # List files in the downloads folder to check for the downloaded file
        files = os.listdir("downloads")
        print("Downloaded files:", files)

        # Find and return the path of the downloaded video file
        for file in files:
            if file.startswith(shortcode) and file.endswith(".mp4"):
                return os.path.join("downloads", file)

        raise Exception("Video file not found after download.")

    except Exception as e:
        print(f"Error downloading reel: {e}")
        # List the downloads folder to check for the file
        files = os.listdir("downloads")
        print("Downloaded files:", files)
