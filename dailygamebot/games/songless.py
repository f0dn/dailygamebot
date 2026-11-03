import re

from ..games import Game


class Songless(Game):
    def __init__(self):
        self.name = "Songless"
        self.regex = re.compile(r"Songless #\d+")
        self.url = "https://less.gg/songless"

    def parse_score(self, message: str) -> int | None:
        if not self.regex:
            return None

        match = self.regex.match(message)
        if match:
            score = 0
            lines = message.split("\n")
            for line in lines[2:7]:
                for i, c in enumerate(line):
                    if c == "\U0001f7e9":
                        score += 5 - i
                        break
            return score
        return None
