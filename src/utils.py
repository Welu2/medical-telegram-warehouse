import json
import os


def create_directory(path):
    """Create a directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def save_json(data, filepath):
    """Save data to a JSON file."""
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def normalize_channel_name(channel_name):
    """Remove '@' from channel names."""
    return channel_name.replace("@", "")