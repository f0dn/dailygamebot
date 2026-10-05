from abc import ABC, abstractmethod


class Game(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def parse_score(self, message: str) -> int | None:
        """
        Parse the score from a message string.

        Args:
            message (str): The message string containing the score.
        Return:
            int | None: The parsed score as an integer, or None if parsing fails.
        """


GAMES: list[Game] = []
