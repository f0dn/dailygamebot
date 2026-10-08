import datetime
import logging

from discord import Client, Intents, Member, TextChannel, User
from discord.ext import tasks

from dailygamebot.games import GAMES

LOGGER = logging.getLogger(__name__)


def run(token: str):
    intents = Intents.default()
    intents.message_content = True

    channels: dict[int, TextChannel] = {}

    client = Client(intents=intents)

    @tasks.loop(seconds=5)
    async def send_recap():
        for guild in client.guilds:
            if guild.id in channels:
                channel = channels[guild.id]

                scores: dict[str, dict[User | Member, int]] = {}
                async for message in channel.history(
                    after=datetime.datetime.now(datetime.UTC)
                    - datetime.timedelta(seconds=5)
                ):
                    if message.author == client.user:
                        continue
                    LOGGER.info(
                        f"Processing message from {message.author}: {message.content}"
                    )
                    for game in GAMES:
                        score = game.parse_score(message.content)
                        if score:
                            LOGGER.info(
                                f"Found score for {game.name}: {score} from {message.author}"
                            )
                            if game.name not in scores:
                                scores[game.name] = {}
                            scores[game.name][message.author] = score
                for game_name, game_scores in scores.items():
                    message = f"Recap for {game_name}:\n"
                    for user, score in sorted(
                        game_scores.items(), key=lambda x: x[1], reverse=True
                    ):
                        message += f"{user.mention}: {score if score != -1 else 'X'}\n"
                    await channel.send(message)

    @client.event
    async def on_ready():
        for guild in client.guilds:
            for channel in guild.text_channels:
                if channel.name == "game-chat":
                    channels[guild.id] = channel
                    break

        send_recap.start()

    client.run(token)
