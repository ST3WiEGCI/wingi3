import os
from dotenv import load_dotenv

load_dotenv()

print("Rocket League Coach")
print("--------------------")
print("Replay Folder:")
print(os.getenv("REPLAY_FOLDER"))

print("\nBallchasing Token Loaded:")

token = os.getenv("BALLCHASING_TOKEN")

if token:
    print(f"Yes ({token[:6]}...)")
else:
    print("No")