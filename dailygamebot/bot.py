import datetime
import logging
from zoneinfo import ZoneInfo

from discord import Client, Intents, Member, Message, TextChannel, User
from discord.ext import tasks

from dailygamebot.games import GAMES, Game

LOGGER = logging.getLogger(__name__)

TIMEZONE = ZoneInfo("America/New_York")
MIDNIGHT = datetime.time(hour=0, minute=0, second=0, tzinfo=TIMEZONE)


def run(token: str):
    intents = Intents.default()
    intents.message_content = True

    channels: dict[int, TextChannel] = {}

    client = Client(intents=intents)

    async def recap(channel: TextChannel):
        scores: dict[Game, dict[User | Member, int]] = {}
        async for message in channel.history(
            after=datetime.datetime.combine(
                datetime.datetime.now(TIMEZONE).date(),
                datetime.time.min,
                tzinfo=TIMEZONE,
            )
        ):
            if message.author == client.user:
                continue
            LOGGER.info(f"Processing message from {message.author}: {message.content}")
            for game in GAMES:
                score = game.parse_score(message.content)
                if score:
                    LOGGER.info(
                        f"Found score for {game.name}: {score} from {message.author}"
                    )
                    if game not in scores:
                        scores[game] = {}
                    scores[game][message.author] = score
        for game, game_scores in scores.items():
            message = f"Recap for {game.name}:\n"
            for user, score in sorted(
                game_scores.items(),
                key=lambda x: x[1],
                reverse=not game.reversed,
            ):
                message += f"{user.mention}: {score if score != -1 else 'X'}\n"
            await channel.send(message)

    @tasks.loop(time=MIDNIGHT)
    async def send_recap(channel: TextChannel | None = None):
        for guild in client.guilds:
            if guild.id in channels:
                channel = channels[guild.id]
                await recap(channel)

    @client.event
    async def on_message(message: Message):
        if message.author == client.user:
            return

        if not message.guild:
            return

        if message.content.startswith("!recap") and message.channel == channels.get(
            message.guild.id
        ):
            LOGGER.info(f"Recap requested by {message.author} in {message.guild.name}")
            channel = channels[message.guild.id]
            await recap(channel)

    @client.event
    async def on_ready():
        for guild in client.guilds:
            for channel in guild.text_channels:
                if channel.name == "game-chat":
                    channels[guild.id] = channel
                    break

        send_recap.start()

    client.run(token, root_logger=True)
