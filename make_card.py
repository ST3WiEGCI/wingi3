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
    return ImageFont.truetype(str(font_path), size) if font_path.exists() else ImageFont.load_default()


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


def opponent_team(data, player_team):
    for team in data["teams"]:
        if team["isOrange"] != player_team["isOrange"]:
            return team

    raise SystemExit("Could not find opponent team.")


def draw_label(draw, label, value, x, y, label_font, value_font):
    draw.text((x, y), label, font=label_font, fill=(150, 180, 255))
    y += 34
    draw.text((x, y), value, font=value_font, fill=(240, 240, 240))
    return y + 70


def choose_debrief(team_size, result, player):
    goals = int(player["goals"])
    assists = int(player["assists"])
    saves = int(player["saves"])
    shots = int(player["shots"])

    if team_size == 1 and result == "LOSS":
        return (
            "1v1 possession discipline.",
            "Prioritize controlled touches over panic clears.",
            "1s said: no teammates, no alibis."
        )

    if team_size == 1 and result == "WIN":
        return (
            "Solo control carried the match.",
            "Keep protecting possession after every challenge.",
            "No teammate needed. Apparently."
        )

    if team_size == 3 and result == "WIN" and assists >= 3:
        return (
            "Playmaker impact.",
            "Keep creating chances without overcommitting.",
            f"{assists} assists? Bro was running air traffic control."
        )

    if result == "WIN" and goals >= 3:
        return (
            "Finisher impact.",
            "Keep converting chances without forcing low-percentage shots.",
            "Net was open for business."
        )

    if result == "WIN" and saves >= 3:
        return (
            "Defensive stability.",
            "Keep buying time and forcing weak shots.",
            "Back line had a supervisor tonight."
        )

    if result == "WIN" and shots >= 5 and goals == 0:
        return (
            "Shot quality check.",
            "Turn pressure into better-placed shots.",
            "The net saw the shots. It remained unimpressed."
        )

    if result == "WIN":
        return (
            "Support-heavy winning role.",
            "Track support, disruption, and staying involved.",
            "Scoreboard saluted."
        )

    if team_size >= 2 and result == "LOSS" and saves >= 3:
        return (
            "Defensive pressure overload.",
            "Reduce panic saves by cutting off pressure earlier.",
            "Goal line was filing overtime paperwork."
        )

    return (
        "Team pressure broke down.",
        "Stay connected and recover through small pads.",
        "The rotation filed a complaint."
    )


def main():
    data = load_summary()
    metadata = data["gameMetadata"]
    team_size = int(metadata["teamSize"])

    player = find_player(data)
    my_team = find_team(data, player)
    opp_team = opponent_team(data, my_team)

    my_score = int(my_team["score"])
    opp_score = int(opp_team["score"])

    result = "WIN" if my_score > opp_score else "LOSS"
    mission_status = "MISSION COMPLETE" if result == "WIN" else "MISSION CONTINUES"

    learning_point, mission, wingman = choose_debrief(team_size, result, player)

    stat_line = f'{player["goals"]}G / {player["assists"]}A / {player["saves"]}S / {player["shots"]} Shots'

    width, height = 1200, 900
    img = Image.new("RGB", (width, height), (15, 18, 24))
    draw = ImageDraw.Draw(img)

    title_font = font(54, True)
    subtitle_font = font(28)
    label_font = font(27, True)
    value_font = font(34)
    small_font = font(25)

    x = 70
    y = 55

    draw.text((x, y), "$T3WiE'z Wingi3", font=title_font, fill=(245, 245, 245))
    y += 65

    draw.text(
        (x, y),
        "Every outcome has a cause. Find it. Learn from it.",
        font=subtitle_font,
        fill=(190, 190, 190)
    )
    y += 55

    draw.line((x, y, width - x, y), fill=(80, 90, 110), width=3)
    y += 40

    y = draw_label(draw, "MISSION STATUS", mission_status, x, y, label_font, value_font)

    y = draw_label(
        draw,
        "MODE / RESULT",
        f"{team_size}v{team_size}  |  {result} {my_score}-{opp_score}",
        x,
        y,
        label_font,
        value_font
    )

    y = draw_label(draw, PLAYER_NAME, stat_line, x, y, label_font, value_font)

    y = draw_label(draw, "LEARNING POINT", learning_point, x, y, label_font, value_font)

    draw.text((x, y), "MISSION", font=label_font, fill=(150, 180, 255))
    y += 34
    draw.text((x, y), mission, font=small_font, fill=(240, 240, 240))
    y += 65

    draw.line((x, y, width - x, y), fill=(80, 90, 110), width=2)
    y += 25

    draw.text((x, y), "WINGMAN", font=label_font, fill=(255, 200, 120))
    y += 34
    draw.text((x, y), wingman, font=value_font, fill=(240, 240, 240))

    output_path = OUTPUT_DIR / "wingi3_card.png"
    img.save(output_path)

    print(f"Created {output_path}")


if __name__ == "__main__":
    main()