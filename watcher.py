import os
import time
import glob
import sqlite3
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BALLCHASING_TOKEN")
REPLAY_FOLDER = os.getenv("REPLAY_FOLDER")
DB = "rlcoach.db"

headers = {"Authorization": TOKEN}


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS replays (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        replay_id TEXT UNIQUE,
        location TEXT,
        local_file TEXT UNIQUE,
        uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def already_uploaded(path):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT 1 FROM replays WHERE local_file = ?", (path,))
    result = cur.fetchone()

    conn.close()
    return result is not None


def save_replay(replay_id, location, path):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT OR IGNORE INTO replays (replay_id, location, local_file)
    VALUES (?, ?, ?)
    """, (replay_id, location, path))

    conn.commit()
    conn.close()


def upload_replay(path):
    print(f"Uploading: {os.path.basename(path)}")

    with open(path, "rb") as f:
        response = requests.post(
            "https://ballchasing.com/api/v2/upload",
            headers=headers,
            files={"file": f},
            data={"visibility": "private"}
        )

    print("Status:", response.status_code)

    try:
        data = response.json()
    except Exception:
        print("Could not read response as JSON.")
        print(response.text)
        return

    if response.status_code == 429 or "quota" in str(data).lower():
        print("Daily Ballchasing upload quota reached. Stopping watcher for today.")
        raise SystemExit

    if response.status_code in (201, 409):
        replay_id = data.get("id")
        location = data.get("location")

        save_replay(replay_id, location, path)

        print("Saved:", location)
    else:
        print("Upload failed:")
        print(data)


def watch():
    init_db()

    print("$T3WiE'z Wingi3 is watching for replays...")
    print(REPLAY_FOLDER)

    while True:
        replays = glob.glob(os.path.join(REPLAY_FOLDER, "*.replay"))
        replays.sort(key=os.path.getmtime)

        for replay in replays:
            if " - Copy" in replay:
                continue

            if time.time() - os.path.getmtime(replay) < 30:
                continue

            if not already_uploaded(replay):
                upload_replay(replay)

        time.sleep(20)


if __name__ == "__main__":
    watch()