from src.utils import create_directory
import os

# Tracks the number of downloaded images globally or per channel
download_counter = 0
IMAGE_LIMIT = 1000  # Set your desired maximum image count here

async def download_image(client, message, channel_name, image_dir):
    """
    Download an image from a Telegram message up to a maximum limit.
    """
    global download_counter

    # 1. Stop if the message has no photo
    if not message.photo:
        return

    # 2. Stop if we have already hit our image limit
    if download_counter >= IMAGE_LIMIT:
        return

    create_directory(f"{image_dir}/{channel_name}")
    file_path = f"{image_dir}/{channel_name}/{message.id}.jpg"

    # 3. Optional: Skip if the file was already downloaded in a previous run
    if os.path.exists(file_path):
        return

    # 4. Download and increment the counter
    await client.download_media(message, file=file_path)
    download_counter += 1
