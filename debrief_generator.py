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
    "dfp": True,
    "event": "Goal Against @ 2:23",
    "rc": "Second-man challenge without support",
    "confidence": 91,
    "cf": [
        "Low boost",
        "Teammate recovering",
        "Wide recovery path"
    ],
    "narrative": "The final save was missed, but the first recoverable decision happened earlier. The second-man challenge occurred before teammate support was available, which collapsed the defensive structure.",
    "mission": "Delay one beat before challenging as second man.",
    "wingman": "Bold strategy. The opponent appreciated the invitation."
}

report = Debrief(facts)
print(report.render())