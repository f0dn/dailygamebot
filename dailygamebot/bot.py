import discord


def run(token):
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        pass

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        message.channel.send(message.content)

    client.run(token)
