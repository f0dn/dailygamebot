import re

import emojis

from ..games import Game


class Clueless(Game):
    def __init__(self):
        self.name = "Clueless"
        self.regex = re.compile(r"I solved Clueless #\d+ in (\S+) guesses")
        self.url = "https://lessgames.com/clueless"
        self.reversed = True

    def parse_score(self, message: str) -> int | None:
        if not self.regex:
            return None

        match = self.regex.match(message)
        if match:
            numbers = {}
            for i in range(10):
                numbers[f"{i}\ufe0f\u20e3"] = i

            text = match.group(1)
            score = 0
            for char in emojis.iter(text):
                score *= 10
                score += numbers.get(char, 0)
            return score
        return None
