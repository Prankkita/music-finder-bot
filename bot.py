import logging
import os
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from utils.download_reel import download_reel
from utils.extract_audio import extract_audio
from utils.song_recognition import recognize_song

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# ACRCloud credentials
HOST = "https://identify-ap-southeast-1.acrcloud.com"  # Ensure the correct host URL
ACCESS_KEY = "b33deb820db35e74521bd9169464e5cc"
ACCESS_SECRET = "EjychtsUsyfOs5amW5xLs5NGiPc8L3T5KtzBTF8w"

async def start(update: Update, _: CallbackContext) -> None:
    """Send a welcome message when the user starts the bot."""
    await update.message.reply_text('Hello! Send me a reel link, and I will recognize the song for you.')

async def handle_reel_link(update: Update, _: CallbackContext) -> None:
    """Handle the reel link and process the song recognition."""
    reel_link = update.message.text
    user = update.message.from_user
    await update.message.reply_text(f'Hi {user.first_name}, downloading the reel...')

    try:
        # Download the reel
        download_path = download_reel(reel_link)

        # Check if the downloaded reel file exists
        if not os.path.exists(download_path):
            raise FileNotFoundError(f"Downloaded reel file not found at {download_path}")

        # Log the file size
        reel_size = os.path.getsize(download_path)
        if reel_size == 0:
            raise Exception(f"Downloaded reel file is empty: {download_path}")
        logger.info(f"Downloaded reel at {download_path}, size: {reel_size} bytes")

        # Send the reel file (MP4) to the user
        reel_file = InputFile(download_path)
        await update.message.reply_video(reel_file, caption="Here's your reel!")

        # Extract audio from the reel
        audio_path = extract_audio(download_path)

        # Check if the audio file exists and is not empty
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found at {audio_path}")
        
        audio_size = os.path.getsize(audio_path)
        if audio_size == 0:
            raise Exception(f"Extracted audio file is empty: {audio_path}")
        
        logger.info(f"Extracted audio at {audio_path}, size: {audio_size} bytes")

        # Send the song's MP3 file (extracted audio) with song details
        song_info = recognize_song(audio_path, HOST, ACCESS_KEY, ACCESS_SECRET)

        # Send the song details back to the user
        if song_info and 'metadata' in song_info:
            song = song_info['metadata']['music'][0]  # Get the first song from the list
            title = song.get('title', 'Unknown Title')
            artists = ', '.join(artist['name'] for artist in song.get('artists', []))
            album = song.get('album', {}).get('name', 'Unknown Album')
            genres = ', '.join(genre['name'] for genre in song.get('genres', []))
            release_date = song.get('release_date', 'Unknown Release Date')
            youtube_link = song.get('external_metadata', {}).get('youtube', {}).get('vid', '')
            spotify_track_id = song.get('external_metadata', {}).get('spotify', {}).get('track', {}).get('id', '')
            
            if spotify_track_id:
                spotify_link = f"https://open.spotify.com/track/{spotify_track_id}"
            else:
                spotify_link = f"https://open.spotify.com/search/{title}"

            # Prepare the song's MP3 file
            song_file = InputFile(audio_path)

            # Create the inline keyboard for YouTube and Spotify links
            keyboard = [
                [
                    InlineKeyboardButton("YouTube", url=f"https://www.youtube.com/watch?v={youtube_link}"),
                    InlineKeyboardButton("Spotify", url=spotify_link)
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            response_message = (
                f"🎶 **Song Found: {title}**\n\n"
                f"- Artists: {artists}\n"
                f"- Album: {album}\n"
                f"- Genres: {genres}\n"
                f"- Release Date: {release_date}\n"
            )

            # Send the MP3 file with the song details and buttons
            await update.message.reply_audio(song_file, caption=response_message, reply_markup=reply_markup)

        else:
            await update.message.reply_text("Sorry, I couldn't recognize the song. Please try again.")

    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    """Start the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token
    application = Application.builder().token("7666502068:AAGaEwx2C8KZjQwritLxDdS66S30CFwCy-k").build()

    # Add command handler for '/start'
    application.add_handler(CommandHandler("start", start))

    # Add message handler for reel link (fixed the filter syntax)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_reel_link))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
