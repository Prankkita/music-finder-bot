import os
import ffmpeg

def extract_audio(video_path):
    """
    Extract audio from the given video file.

    Args:
        video_path (str): The path to the video file.
        
    Returns:
        str: The file path to the extracted audio.
    """
    try:
        # Define output file path
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        audio_path = os.path.join(output_dir, f"{base_name}.mp3")

        # Use FFmpeg to extract audio
        ffmpeg.input(video_path).output(audio_path, format="mp3", acodec="libmp3lame").run(overwrite_output=True)
        
        if not os.path.exists(audio_path):
            raise Exception("Audio extraction failed.")
        
        return audio_path
    except Exception as e:
        raise Exception(f"Error extracting audio: {e}")
