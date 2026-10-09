import re

from ..games import Game


class DontWordle(Game):
    def __init__(self):
        self.name = "Don't Wordle"
        self.regex = re.compile(r"Don't Wordle \d+ - (\w+)")

    def parse_score(self, message: str) -> int | None:
        match = self.regex.match(message)
        if match:
            if match.group(1) == "WORDLED":
                return -1
            try:
                return int(message.split("\n")[12].split()[1])
            except ValueError:
                return -1
        return None
