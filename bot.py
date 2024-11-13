import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Load configurations
from config import API_ID, API_HASH, BOT_TOKEN, CR_USERNAME, CR_PASSWORD

# Initialize the bot client
app = Client("crunchyroll_downloader_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command to start the download process
@app.on_message(filters.command("download"))
async def download_video(client: Client, message: Message):
    # Ensure a link is provided
    if len(message.command) < 2:
        await message.reply("Please provide a Crunchyroll video link after /download.")
        return

    crunchyroll_url = message.command[1]
    await message.reply("Starting download...")

    # Execute multi-downloader-nx with credentials
    download_command = [
        "python3", "multi-downloader-nx/multi_downloader.py",
        "--service", "crunchyroll",
        "--username", CR_USERNAME,
        "--password", CR_PASSWORD,
        "--url", crunchyroll_url,
        "--output", "downloads"
    ]

    try:
        # Start the download process
        process = subprocess.run(download_command, check=True, capture_output=True, text=True)

        # Check if the file downloaded
        output_dir = "downloads"
        downloaded_files = os.listdir(output_dir)
        if downloaded_files:
            video_path = os.path.join(output_dir, downloaded_files[0])

            # Send the video to the user
            await message.reply_video(video=video_path, caption="Here is your downloaded video.")
            
            # Clean up the download directory
            os.remove(video_path)
        else:
            await message.reply("Download failed or no video found.")

    except subprocess.CalledProcessError as e:
        await message.reply(f"Download error: {e.output}")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Start the bot
app.run()
