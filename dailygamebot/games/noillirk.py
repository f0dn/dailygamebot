import re

from ..games import Game


class Noillirk(Game):
    def __init__(self):
        self.name = "Noillirk"
        self.regex = re.compile(r"Noillirk - ([\d,]+)m")
        self.url = "https://playdaily.org/noillirk"
