import os
import glob
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BALLCHASING_TOKEN")
REPLAY_FOLDER = os.getenv("REPLAY_FOLDER")

headers = {
    "Authorization": TOKEN
}

replays = glob.glob(os.path.join(REPLAY_FOLDER, "*.replay"))

if not replays:
    print("No replay files found.")
    raise SystemExit

latest_replay = max(replays, key=os.path.getmtime)

print(f"Uploading latest replay:")
print(latest_replay)

with open(latest_replay, "rb") as f:
    files = {
        "file": f
    }
    data = {
        "visibility": "private"
    }

    response = requests.post(
        "https://ballchasing.com/api/v2/upload",
        headers=headers,
        files=files,
        data=data
    )

print("Status:", response.status_code)
print(response.text)