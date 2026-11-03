import json
import sys
from pathlib import Path

from dailygamebot.games import GAMES, Game

MESSAGES = Path(__file__).parent.parent / "tests" / "messages.json"


def add_case(message: str, game: Game, score: int):
    with open(MESSAGES, "r") as f:
        data = json.load(f)
    data.append(
        {
            "message": message,
            "expected_game": game.name,
            "expected_data": score,
        }
    )
    with open(MESSAGES, "w") as f:
        json.dump(data, f, indent=4)


def add_test():
    print("Paste message:")
    message = sys.stdin.read().rstrip()

    matched = False
    for game in GAMES:
        score = game.parse_score(message)
        if score:
            matched = True
            print(f"{game.name} parsed this message with a score of {score}")
            correct = input("Is this correct? (y/n): ")
            if correct.lower() in ("y", "yes"):
                print("Message added to testcases.")
                add_case(message, game, score)
                break
            else:
                print("Message not added to testcases.")
                break
    if not matched:
        print("No game matched this message.")


if __name__ == "__main__":
    add_test()
