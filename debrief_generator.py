class Debrief:
    def __init__(self, facts):
        self.facts = facts

    def render(self):
        if self.facts.get("dfp"):
            return self.render_dfp()
        return self.render_learning_point()

    def render_dfp(self):
        cf_lines = "\n".join(f"- {cf}" for cf in self.facts["cf"])

        return f"""
$T3WiE'z Wingi3

EVENT
{self.facts["event"]}

RC
{self.facts["rc"]}

CONFIDENCE
{self.facts["confidence"]}%

CF
{cf_lines}

NARRATIVE
{self.facts["narrative"]}

MISSION
{self.facts["mission"]}

WINGMAN
{self.facts["wingman"]}
"""

    def render_learning_point(self):
        return f"""
$T3WiE'z Wingi3

LEARNING POINT
{self.facts["learning_point"]}

NARRATIVE
{self.facts["narrative"]}

MISSION
{self.facts["mission"]}

WINGMAN
{self.facts["wingman"]}
"""


facts = {
    "dfp": False,
    "learning_point": "Stay connected after your first challenge",
    "narrative": "Across the session, the key improvement area was staying connected to the play after the first challenge. The issue was not one single goal against, but a repeated tendency to rotate too far away from pressure instead of using small pads to remain available.",
    "mission": "After each first challenge, collect small pads and stay within one playable touch of the ball.",
    "wingman": "Corner boost filed a missing persons report."
}

report = Debrief(facts)
print(report.render())