import re

from ..games import Game


class Spellcheck(Game):
    def __init__(self):
        self.name = "Spellcheck"
        self.regex = re.compile(r"Spellcheck #\d+")
        self.url = "https://spellcheck.xyz"

    def parse_score(self, message: str) -> int | None:
        if not self.regex:
            return None

        match = self.regex.match(message)
        if match:
            score = 0
            lines = message.split("\n")
            for line in lines[1:4]:
                for c in line:
                    if c == "\U0001f7e9":
                        score += 1
            return score
        return None
