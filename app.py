import discord
import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents().all()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_update(before, after):
    print("test")
    if before.status is discord.Status.offline and after.status is discord.Status.online:
        print('was offline then online')
        channel = client.get_channel(845354528819118121)  # notification channel
        await channel.send(f'{after.name} is now {after.status}')

client.run(os.getenv('TOKEN'))