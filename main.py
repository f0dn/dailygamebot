import os
from sys import argv

from dotenv import load_dotenv

from dailygamebot.bot import run


def main():
    if len(argv) > 1 and argv[1] == "add_test":
        from scripts.add_test import add_test

        add_test()
        return

    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")

    if token:
        run(token)
    else:
        print("Error: DISCORD_TOKEN not found in environment variables.")


if __name__ == "__main__":
    main()
