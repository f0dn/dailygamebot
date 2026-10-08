import re

from ..games import Game


class Sedecordle(Game):
    def __init__(self):
        self.name = "Sedecordle"

    def parse_score(self, message: str) -> int | None:
        match = re.match(r"Daily Sedecordle #\d+\nGuesses: (\w+)/\d+", message)
        if match:
            try:
                score = int(match.group(1))
                return score
            except ValueError:
                return -1
