import random

mission_status = random.choice(["Mission Complete", "Mission Continues"])

learning_points = [
    "Stay connected to the play.",
    "Delay your second-man challenge.",
    "Collect small pads before leaving for corner boost.",
    "Recover immediately after a missed demo.",
    "Take one controlled touch before booming the ball."
]

wingman = [
    "😂 Debrief Note: The opponent appreciates your generous possession donation.",
    "😂 Debrief Note: Ball contact remains highly encouraged.",
    "😂 Debrief Note: Target escaped. Physics was involved.",
    "😂 Debrief Note: That challenge had confidence. Evidence is still under review.",
    "😂 Debrief Note: The replay has been forwarded to NASA for trajectory analysis."
]

print("="*45)
print("        $T3WiE'z Wingi3")
print(" Every outcome has a cause.")
print(" Find it. Learn from it.")
print("="*45)

print()
print("MISSION STATUS")
print(mission_status)

print()
print("LEARNING POINT")
print(random.choice(learning_points))

print()
print("MISSION")
print("Focus ONLY on that learning point next session.")

print()
print(random.choice(wingman))

print("="*45)