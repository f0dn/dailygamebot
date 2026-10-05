import datetime

from discord import Client, Intents, TextChannel
from discord.ext import tasks


def run(token: str):
    intents = Intents.default()
    intents.message_content = True

    channels: dict[int, TextChannel] = {}

    client = Client(intents=intents)

    @tasks.loop(seconds=5)
    async def send_recap():
        print("hello")
        for guild in client.guilds:
            if guild.id in channels:
                channel = channels[guild.id]
                count = 0
                async for message in channel.history(
                    after=datetime.datetime.now(datetime.UTC)
                    - datetime.timedelta(seconds=5)
                ):
                    count += 1
                await channel.send("count: " + str(count))

    @client.event
    async def on_ready():
        for guild in client.guilds:
            for channel in guild.text_channels:
                if channel.name == "game-chat":
                    channels[guild.id] = channel
                    break

    client.run(token)
