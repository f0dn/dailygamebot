import os

from dotenv import load_dotenv

from dailygamebot.bot import run


def main():
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")

    run(token)


if __name__ == "__main__":
    main()
