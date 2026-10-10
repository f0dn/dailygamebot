import re

from ..games import Game


class Sedecordle(Game):
    def __init__(self):
        self.name = "Sedecordle"
        self.regex = re.compile(r"Daily Sedecordle #\d+\nGuesses: (\w+)/\d+")
        self.reversed = True
