import asyncio
import os
from datetime import datetime

from telethon.errors import FloodWaitError

from src.telegram_client import client
from src.config import CHANNELS, RAW_DATA_DIR, IMAGE_DIR
from src.logger import logger
from src.utils import create_directory, save_json
from src.image_downloader import download_image


async def scrape_channel(channel_name):
    logger.info(f"Scraping {channel_name}")

    today = datetime.now().strftime("%Y-%m-%d")
    json_directory = os.path.join(RAW_DATA_DIR, today)
    create_directory(json_directory)

    filename = channel_name.replace("@", "") + ".json"
    filepath = os.path.join(json_directory, filename)

    records = []
    message_count = 0
    MAX_MESSAGES = 150  # Hard limit to quickly verify it works

    try:
        # Added a limit parameter here to avoid infinite processing loops
        async for message in client.iter_messages(channel_name, limit=MAX_MESSAGES):
            record = {
                "message_id": message.id,
                "date": str(message.date),
                "text": message.text,
                "views": message.views,
                "forwards": message.forwards,
                "has_media": message.media is not None,
            }
            records.append(record)
            message_count += 1

            if message.media:
                await download_image(
                    client,
                    message,
                    channel_name.replace("@", ""),
                    IMAGE_DIR
    )

            # Pro-Tip: Save every 50 messages so you don't lose data if it crashes
            if message_count % 50 == 0:
                save_json(records, filepath)
                logger.info(f"Checkpoint: Saved {message_count} messages for {channel_name}")

        # Final save for the remaining messages
        if records:
            save_json(records, filepath)
            logger.info(f"Finalized: {channel_name}: {len(records)} messages saved safely.")

    except FloodWaitError as e:
        logger.warning(f"Flood wait {e.seconds} seconds encountered.")
        await asyncio.sleep(e.seconds)
    except Exception as e:
        logger.exception(e)

async def main():

    await client.start()

    logger.info("Telegram client started.")

    for channel in CHANNELS:
        await scrape_channel(channel)

    logger.info("Scraping completed.")

    await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())