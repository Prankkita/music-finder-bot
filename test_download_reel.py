import os
import instaloader

def download_reel(reel_url):
    loader = instaloader.Instaloader(dirname_pattern="downloads", filename_pattern="{shortcode}")
    try:
        loader.download_post(instaloader.Post.from_shortcode(loader.context, reel_url.split("/")[-2]), target="downloads")
        print("Reel downloaded successfully.")
    except Exception as e:
        print(f"Error downloading reel: {e}")
        # List the downloads folder to check for the file
        files = os.listdir("downloads")
        print("Downloaded files:", files)

# Get the reel URL
reel_url = input("Enter the Instagram reel URL: ")
download_reel(reel_url)