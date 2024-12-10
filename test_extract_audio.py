from utils.extract_audio import extract_audio

if __name__ == "__main__":
    video_path = input("Enter the path to the video file: ")
    try:
        audio_path = extract_audio(video_path)
        print(f"Audio extracted successfully: {audio_path}")
    except Exception as e:
        print(f"Failed to extract audio: {e}")
