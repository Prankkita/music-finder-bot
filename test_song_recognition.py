from utils.song_recognition import recognize_song

if __name__ == "__main__":
    audio_path = input("Enter the path to the audio file: ")

    # Add your ACRCloud credentials
    HOST = "https://identify-ap-southeast-1.acrcloud.com"  # Make sure the host URL starts with https://
    ACCESS_KEY = "b33deb820db35e74521bd9169464e5cc"
    ACCESS_SECRET = "EjychtsUsyfOs5amW5xLs5NGiPc8L3T5KtzBTF8w"

    try:
        result = recognize_song(audio_path, HOST, ACCESS_KEY, ACCESS_SECRET)
        print("Song Recognition Result:")
        print(result)
    except Exception as e:
        print(f"Failed to recognize song: {e}")
