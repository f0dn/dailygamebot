import re

from ..games import Game


class Duotrigordle(Game):
    def __init__(self):
        self.name = "Duotrigordle"
        self.regex = re.compile(r"Daily Duotrigordle #\d+\nGuesses: (\w+)/\d+")
