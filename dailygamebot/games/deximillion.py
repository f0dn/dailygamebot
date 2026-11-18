import re

from ..games import Game


class Deximillion(Game):
    def __init__(self):
        self.name = "Deximillion"
        self.regex = re.compile(r"DEXIMILLION \d+-\d+-\d+")
        self.url = "https://pokemillion.com"

    def parse_score(self, message: str) -> int | None:
        if not self.regex:
            return None

        match = self.regex.match(message)
        if match:
            line = message.split("\n")[2]
            if "caught it!" in line:
                try:
                    return int(line.split()[3])
                except ValueError:
                    return -1
            else:
                return -1
        return None
