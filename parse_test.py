import os
import json
import glob
import carball
from dotenv import load_dotenv

load_dotenv()

replay_folder = os.getenv("REPLAY_FOLDER")

if not replay_folder:
    raise SystemExit("REPLAY_FOLDER is missing from .env")

replays = glob.glob(os.path.join(replay_folder, "*.replay"))

if not replays:
    raise SystemExit("No replay files found.")

latest_replay = max(replays, key=os.path.getmtime)

print("Summarizing latest replay:")
print(latest_replay)

summary = carball.summarize_replay_file(latest_replay)
data = summary.get_json_data()

with open("replay_summary.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, default=str)

print("Created real replay_summary.json")