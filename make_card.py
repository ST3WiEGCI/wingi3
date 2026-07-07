import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

SUMMARY_FILE = Path("replay_summary.json")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

PLAYER_NAME = "$T3WiE"


def font(size, bold=False):
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    font_path = Path("C:/Windows/Fonts") / font_name

    if font_path.exists():
        return ImageFont.truetype(str(font_path), size)

    return ImageFont.load_default()


def load_summary():
    with open(SUMMARY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def find_player(data):
    for player in data["players"]:
        if player["name"] == PLAYER_NAME:
            return player

    raise SystemExit(f"Could not find player named {PLAYER_NAME}")


def find_team(data, player):
    player_id = player["id"]["id"]

    for team in data["teams"]:
        team_ids = [p["id"] for p in team["playerIds"]]
        if player_id in team_ids:
            return team

    raise SystemExit("Could not find player's team.")


def get_opponent_team(data, player_team):
    for team in data["teams"]:
        if team["isOrange"] != player_team["isOrange"]:
            return team

    raise SystemExit("Could not find opponent team.")


def draw_text(draw, text, xy, font_obj, fill=(240, 240, 240)):
    draw.text(xy, text, font=font_obj, fill=fill)


def main():
    data = load_summary()
    metadata = data["gameMetadata"]

    player = find_player(data)
    player_team = find_team(data, player)
    opponent_team = get_opponent_team(data, player_team)

    player_score = player_team["score"]
    opponent_score = opponent_team["score"]

    result = "WIN" if player_score > opponent_score else "LOSS"
    mission_status = "MISSION COMPLETE" if result == "WIN" else "MISSION CONTINUES"

    stat_line = f'{player["goals"]}G / {player["assists"]}A / {player["saves"]}S / {player["shots"]} Shots'

    width, height = 1200, 675
    img = Image.new("RGB", (width, height), (15, 18, 24))
    draw = ImageDraw.Draw(img)

    title_font = font(54, bold=True)
    subtitle_font = font(28)
    section_font = font(28, bold=True)
    body_font = font(34)
    small_font = font(24)

    x = 70
    y = 55

    draw_text(draw, "$T3WiE'z Wingi3", (x, y), title_font)
    y += 65

    draw_text(draw, "Every outcome has a cause. Find it. Learn from it.", (x, y), subtitle_font, (190, 190, 190))
    y += 55

    draw.line((x, y, width - x, y), fill=(80, 90, 110), width=3)
    y += 40

    draw_text(draw, "MISSION STATUS", (x, y), section_font, (150, 180, 255))
    y += 38
    draw_text(draw, mission_status, (x, y), body_font)
    y += 60

    draw_text(draw, "MODE / RESULT", (x, y), section_font, (150, 180, 255))
    y += 38
    draw_text(draw, f'{metadata["teamSize"]}v{metadata["teamSize"]}  |  {result} {player_score}-{opponent_score}', (x, y), body_font)
    y += 60

    draw_text(draw, PLAYER_NAME, (x, y), section_font, (150, 180, 255))
    y += 38
    draw_text(draw, stat_line, (x, y), body_font)
    y += 60

    draw_text(draw, "LEARNING POINT", (x, y), section_font, (150, 180, 255))
    y += 38
    draw_text(draw, "Support-heavy winning role.", (x, y), body_font)
    y += 60

    draw_text(draw, "MISSION", (x, y), section_font, (150, 180, 255))
    y += 38
    draw_text(draw, "Track support, disruption, and staying involved.", (x, y), small_font)

    y = height - 95
    draw.line((x, y - 25, width - x, y - 25), fill=(80, 90, 110), width=2)
    draw_text(draw, "WINGMAN", (x, y), section_font, (255, 200, 120))
    draw_text(draw, "Scoreboard saluted. 🫡", (x + 185, y), section_font)

    output_path = OUTPUT_DIR / "wingi3_card.png"
    img.save(output_path)

    print(f"Created {output_path}")


if __name__ == "__main__":
    main()