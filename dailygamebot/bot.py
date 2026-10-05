import datetime

import schedule
from discord import Client, Intents, TextChannel


def run(token: str):
    intents = Intents.default()
    intents.message_content = True

    channels: dict[int, TextChannel] = {}

    client = Client(intents=intents)

    async def send_recap():
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

        # schedule.every(1).day.at("00:00").do(send_recap, client)
        schedule.every(5).seconds.do(send_recap, client)

    client.run(token)
