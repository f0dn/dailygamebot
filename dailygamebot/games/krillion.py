import re

from ..games import Game


class Krillion(Game):
    def __init__(self):
        self.name = "Krillion"

    def parse_score(self, message: str) -> int | None:
        match = re.match(r"Krillion #\d+", message)
        if match:
            try:
                score = int(message.split("\n")[1])
                return score
            except ValueError:
                return None
