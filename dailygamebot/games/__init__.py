import importlib
import inspect
import json
import re
from abc import ABC
from pathlib import Path
from re import Pattern


class Game(ABC):
    name: str
    regex: Pattern | None
    reversed: bool = False
    url: str | None = None

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
                return int(match.group(1).replace(",", ""))
            except ValueError:
                return -1
        return None


def load_games() -> list[Game]:
    games_path = Path(__file__).parent / "games.json"
    with open(games_path, "r", encoding="utf-8") as f:
        games_data = json.load(f)

    games = []
    for game_data in games_data:
        game_class = type(
            game_data["name"],
            (Game,),
            {
                "name": game_data["name"],
                "regex": None
                if game_data["regex"] is None
                else re.compile(game_data["regex"]),
                "reversed": game_data.get("reversed", False),
                "url": game_data.get("url"),
            },
        )
        games.append(game_class())

    for path in Path(__file__).parent.glob("*.py"):
        module_name = path.stem
        if module_name in ("__init__", "__pycache__") or module_name.startswith("_"):
            continue
        module = importlib.import_module(f"{__package__}.{module_name}")
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Game) and obj is not Game:
                games.append(obj())
    return games


GAMES = load_games()
