import datetime
import logging
from zoneinfo import ZoneInfo

from discord import Embed, Intents, Interaction, Member, TextChannel, User
from discord.ext import commands, tasks

from dailygamebot.games import GAMES, Game

LOGGER = logging.getLogger(__name__)

TIMEZONE = ZoneInfo("America/New_York")
MIDNIGHT = datetime.time(hour=23, minute=59, second=59, tzinfo=TIMEZONE)


def run(token: str):
    intents = Intents.default()
    intents.message_content = True

    channels: dict[int, TextChannel] = {}

    bot = commands.Bot(command_prefix="/", intents=intents)

    @bot.tree.command(description="Get a recap of the scores for today")
    async def recap(interaction: Interaction):
        if interaction.guild is None:
            await interaction.response.send_message(
                "This command can only be used in a server.", ephemeral=True
            )
            return

        if interaction.guild.id not in channels:
            await interaction.response.send_message(
                "No game-chat channel found for this server.", ephemeral=True
            )
            return

        if interaction.channel != channels[interaction.guild.id]:
            await interaction.response.send_message(
                "This command can only be used in the game-chat channel.",
                ephemeral=True,
            )
            return

        channel = channels[interaction.guild.id]
        LOGGER.info(
            f"Recap requested by {interaction.user} in {interaction.guild.name}"
        )
        embed = await _recap(channel)
        await interaction.response.send_message(embed=embed)

    async def _recap(channel: TextChannel) -> Embed:
        LOGGER.info(f"Starting recap task for {channel.guild.name}")
        scores: dict[Game, dict[User | Member, int]] = {}
        async for message in channel.history(
            after=datetime.datetime.combine(
                datetime.datetime.now(TIMEZONE).date(),
                datetime.time.min,
                tzinfo=TIMEZONE,
            ),
            limit=None,
        ):
            if message.author == bot.user:
                continue
            LOGGER.info(f"Processing message from {message.author}: {message.id}")
            for game in GAMES:
                score = game.parse_score(message.content)
                if score:
                    LOGGER.info(
                        f"Found score for {game.name}: {score} from {message.author}"
                    )
                    if game not in scores:
                        scores[game] = {}
                    scores[game][message.author] = score
        message = ""
        for game, game_scores in scores.items():
            game_name = game.name
            if game.url:
                game_name = f"[{game.name}]({game.url})"
            message += f"Recap for {game_name}:\n"
            for user, score in sorted(
                game_scores.items(),
                key=lambda x: x[1],
                reverse=not game.reversed,
            ):
                message += f"{user.mention}: {score if score != -1 else 'X'}\n"
            message += "\n"
            LOGGER.info(f"Sending recap message to {channel.guild.name}")
        return Embed(description=message.rstrip())

    @tasks.loop(time=MIDNIGHT)
    async def send_recap(channel: TextChannel | None = None):
        LOGGER.info("Starting daily recap task")
        for guild in bot.guilds:
            if guild.id in channels:
                channel = channels[guild.id]
                embed = await _recap(channel)
                await channel.send(embed=embed)

    @bot.event
    async def on_ready():
        for guild in bot.guilds:
            for channel in guild.text_channels:
                if channel.name == "game-chat":
                    LOGGER.info(
                        f"Found game-chat channel in {guild.name}: {channel.name}"
                    )
                    channels[guild.id] = channel
                    break

        send_recap.start()

    @bot.event
    async def setup_hook():
        await bot.tree.sync()
        LOGGER.info("Command tree synced globally")

    bot.run(token, root_logger=True)
