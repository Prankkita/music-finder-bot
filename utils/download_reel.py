import instaloader
import os

def download_reel(reel_url):
    """
    Download an Instagram reel using the provided URL.
    
    Args:
        reel_url (str): The URL of the Instagram reel.
        
    Returns:
        str: The file path to the downloaded reel.
    """
    try:
        # Initialize instaloader
        loader = instaloader.Instaloader()

        # Extract the shortcode from the URL
        shortcode = reel_url.split("/")[-2]

        # Define download directory
        download_dir = "downloads"
        os.makedirs(download_dir, exist_ok=True)

        # Load post using shortcode
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        # Define video file path
        video_path = os.path.join(download_dir, f"{shortcode}.mp4")

        # Download video only
        loader.download_post(post, target=download_dir)
        for file in os.listdir(download_dir):
            if file.startswith(shortcode) and file.endswith(".mp4"):
                return os.path.join(download_dir, file)

        raise Exception("Video file not found after download.")
    except Exception as e:
        raise Exception(f"Error downloading reel: {e}")
