import re

from ..games import Game


class TimeGuessr(Game):
    def __init__(self):
        self.name = "TimeGuessr"

    def parse_score(self, message: str) -> int | None:
        match = re.match(r"TimeGuessr #\d+ — (\d+)/50000", message.replace(",", ""))
        if match:
            try:
                score = int(match.group(1))
                return score
            except ValueError:
                return None
