import os

from dotenv import load_dotenv

from dailygamebot.bot import run


def main():
    load_dotenv()

    token = os.getenv("DISCORD_TOKEN")

    if token:
        run(token)
    else:
        print("Error: DISCORD_TOKEN not found in environment variables.")


if __name__ == "__main__":
    main()
