import json
from pathlib import Path

import pytest

from dailygamebot.games import GAMES


def load_data():
    with open(Path(__file__).parent / "messages.json", "r") as f:
        return json.load(f)


messages = load_data()


@pytest.mark.parametrize("case", messages)
def test_parse(case):
    message = case["message"]
    expected_game = case["expected_game"]
    expected_data = case["expected_data"]

    data = None
    for game in GAMES:
        new_data = game.parse_score(message)
        if new_data is not None:
            assert game.name == expected_game
            assert new_data == expected_data
            data = new_data
    if data is None:
        assert expected_game is None
        assert expected_data is None
