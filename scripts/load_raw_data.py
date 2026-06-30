import os
import json
from pathlib import Path

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Read from Docker injected variables first; fallback to .env config if running locally
DB_NAME = os.getenv("DB_NAME") or os.getenv("POSTGRES_DB")
DB_USER = os.getenv("DB_USER") or os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD") or os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("DB_HOST") or os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("DB_PORT") or os.getenv("POSTGRES_PORT", "5432")

DATA_DIR = Path("data")


def connect():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
    )


def create_schema(cursor):
    cursor.execute(
        """
        CREATE SCHEMA IF NOT EXISTS raw;
        """
    )


def create_table(cursor):
    # CRITICAL FIX: Dropping the old table layout to clear the old single primary key conflict
    cursor.execute("DROP TABLE IF EXISTS raw.telegram_messages CASCADE;")
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS raw.telegram_messages (
            id BIGINT,
            channel_name TEXT,
            channel_username TEXT,
            message TEXT,
            message_date TIMESTAMP,
            views INTEGER,
            forwards INTEGER,
            has_image BOOLEAN,
            image_path TEXT,
            raw_json JSONB,
            PRIMARY KEY (channel_username, id) -- FIXED: Matches ON CONFLICT specification
        );
        """
    )


def load_json_file(cursor, filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 1. Safe metadata extraction based on data type
    if isinstance(data, dict):
        top_channel_name = data.get("name") or filepath.stem
        top_channel_user = data.get("username") or data.get("channel_username") or filepath.stem
        
        # Extract messages array from nested structures
        if "messages" in data:
            records = data["messages"]
        elif "chats" in data:
            records = data.get("chats", {}).get("messages", [])
        else:
            records = [data]
    elif isinstance(data, list):
        # If the file is a direct list, fall back to using the file name
        top_channel_name = filepath.stem
        top_channel_user = filepath.stem
        records = data
    else:
        records = []

    for row in records:
        # Skip invalid non-dictionary rows inside the array
        if not isinstance(row, dict):
            continue

        msg_id = row.get("message_id") or row.get("id")
        if msg_id is None:
            continue

        message_content = row.get("text") or row.get("message")
        if isinstance(message_content, list):
            parsed_text = []
            for item in message_content:
                if isinstance(item, dict):
                    parsed_text.append(item.get("text", ""))
                else:
                    parsed_text.append(str(item))
            message_content = "".join(parsed_text)

        # Use top-level metadata if row-level properties are absent
        channel_name = row.get("channel_name") or top_channel_name
        channel_user = row.get("channel_username") or top_channel_user

        has_img = row.get("has_media") or row.get("has_image", False)

        cursor.execute(
            """
            INSERT INTO raw.telegram_messages
            (
                id, channel_name, channel_username, message,
                message_date, views, forwards, has_image, image_path, raw_json
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (channel_username, id) DO NOTHING;
            """,
            (
                msg_id,
                channel_name,
                channel_user,
                message_content,
                row.get("date"),
                row.get("views") or 0,
                row.get("forwards") or 0,
                has_img,
                row.get("image_path"),
                json.dumps(row),
            ),
        )


def main():
    conn = connect()
    cur = conn.cursor()

    create_schema(cur)
    create_table(cur)
    conn.commit() # Save the schema blueprint changes immediately

    files = sorted(DATA_DIR.rglob("*.json"))

    print(f"Found {len(files)} JSON files")

    for file in files:
        print(f"Loading {file.name}")
        try:
            load_json_file(cur, file)
            conn.commit() # Progressively commit each file so a single crash won't wipe progress
            print(f"Successfully loaded {file.name}")
        except Exception as e:
            conn.rollback()
            print(f"Skipped {file.name} due to an error: {e}")

    cur.close()
    conn.close()

    print("Finished loading raw telegram data.")


if __name__ == "__main__":
    main()
