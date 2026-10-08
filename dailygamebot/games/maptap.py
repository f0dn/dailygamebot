import re

from ..games import Game


class MapTap(Game):
    def __init__(self):
        self.name = "MapTap"
        self.regex = re.compile(r"www.maptap.gg .*\n.*\nFinal score: (\d+)")
