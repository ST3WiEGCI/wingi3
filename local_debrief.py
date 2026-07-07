import json
from pathlib import Path

SUMMARY_FILE = Path("replay_summary.json")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

PLAYER_NAME = "$T3WiE"


def load_summary():
    if not SUMMARY_FILE.exists():
        raise SystemExit("Missing replay_summary.json. Run parse_test.py first.")

    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_player(data, player_name):
    for player in data["players"]:
        if player["name"] == player_name:
            return player
    raise SystemExit(f"Could not find player named {player_name}")


def find_team(data, player):
    player_id = player["id"]["id"]

    for team in data["teams"]:
        team_player_ids = [p["id"] for p in team["playerIds"]]
        if player_id in team_player_ids:
            return team

    raise SystemExit("Could not find player's team.")


def get_opponent_team(data, player_team):
    for team in data["teams"]:
        if team["isOrange"] != player_team["isOrange"]:
            return team

    raise SystemExit("Could not find opponent team.")


def build_debrief(data):
    metadata = data["gameMetadata"]
    player = find_player(data, PLAYER_NAME)
    player_team = find_team(data, player)
    opponent_team = get_opponent_team(data, player_team)

    player_score = player_team["score"]
    opponent_score = opponent_team["score"]

    result = "Win" if player_score > opponent_score else "Loss"
    mission_status = "Complete" if result == "Win" else "Continues"

    analysis_valid = not metadata.get("isInvalidAnalysis", False)

    if analysis_valid:
        learning_point = "Review full replay telemetry."
    else:
        learning_point = "Support-heavy winning role."

    debrief = f"""
$T3WiE'z Wingi3
Every outcome has a cause.
Find it. Learn from it.

MISSION STATUS
{mission_status}

MODE
{metadata["teamSize"]}v{metadata["teamSize"]}

RESULT
{result} {player_score}-{opponent_score}

PLAYER
{player["name"]}

STAT LINE
{player["goals"]}G / {player["assists"]}A / {player["saves"]}S / {player["shots"]} Shots

LEARNING POINT
{learning_point}

NARRATIVE
Full telemetry was not available, so no DFP, RC, or CF should be assigned. Based on summary data only, this match shows useful team contribution: scoring, assisting, and defending without needing to carry the scoreboard.

MISSION
Track whether your best games come from support, disruption, and staying involved.

WINGMAN
You didn't top-frag the scoreboard, but the scoreboard still saluted. 🫡
""".strip()

    return debrief


def main():
    data = load_summary()
    debrief = build_debrief(data)

    print(debrief)

    output_file = OUTPUT_DIR / "discord_debrief.txt"
    output_file.write_text(debrief, encoding="utf-8")

    print()
    print(f"Saved Discord debrief to: {output_file}")


if __name__ == "__main__":
    main()