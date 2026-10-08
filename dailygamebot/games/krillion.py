import re

from ..games import Game


class Krillion(Game):
    def __init__(self):
        self.name = "Krillion"
        self.regex = re.compile(r"Krillion #\d+.*\n(\d+)")
