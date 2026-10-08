from abc import ABC
from re import Pattern


class Game(ABC):
    def __init__(self, name: str, regex: Pattern | None = None):
        self.name = name
        self.regex = regex

    def parse_score(self, message: str) -> int | None:
        """
        Parse the score from a message string.

        Args:
            message (str): The message string containing the score.
        Return:
            int | None: The parsed score as an integer, or None if parsing fails.
        """
        if self.regex is None:
            raise NotImplementedError(
                "Subclasses must implement parse_score if regex is not provided."
            )
        match = self.regex.match(message)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                return -1
        return None


from .krillion import Krillion
from .maptap import MapTap
from .sedecordle import Sedecordle
from .timeguessr import TimeGuessr

GAMES = [Krillion(), TimeGuessr(), Sedecordle(), MapTap()]
