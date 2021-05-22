import datetime
import discord
from discord.ext import tasks
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents().all()
awake = False
streak = 0
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    is_awake.start()

@client.event
async def on_member_update(before, after):
    global awake
    if awake:
        return
    if after.id == int(os.getenv('USERID')):
        awake = True

@tasks.loop(seconds=10)
async def is_awake():
    global awake
    global streak

    channel = client.get_channel(int(os.getenv('CHANNELID')))  # notification channel
    time_now = datetime.datetime.now().time()
    if time_now > datetime.time(4,55) and time_now < datetime.time(5,0):
        await asyncio.sleep(900)
        if not awake:
            await channel.send(f'<@{os.getenv("SENDERID")}> Michael did not wake up, sending £5 to <@{os.getenv("RECEIVERID")}>')
            streak = 0
        else:
            streak += 1
            await channel.send(f'<@{os.getenv("SENDERID")}> has woke up at 5am for {streak} days in a row!')
    awake = False
    return

client.run(os.getenv('TOKEN'))

