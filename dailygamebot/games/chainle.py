import re

from ..games import Game


class Chainle(Game):
    def __init__(self):
        self.name = "Chainle"
        self.regex = re.compile(r"Chainle #\d+ · ([\d,]+)")
