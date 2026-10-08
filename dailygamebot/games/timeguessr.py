import re

from ..games import Game


class TimeGuessr(Game):
    def __init__(self):
        self.name = "TimeGuessr"
        self.regex = re.compile(r"TimeGuessr #\d+ — [\d,]+/50,000")
