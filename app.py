# This code ಠ_ಠ fml

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
async def on_message(message):
    global awake
    if awake:
        return
    if int(message.author.id) == int(os.getenv('USERID')):
        awake = True

@tasks.loop(seconds=100)
async def is_awake():
    global awake
    global streak

    channel = client.get_channel(int(os.getenv('CHANNELID')))  # notification channel
    time_now = datetime.datetime.now().time()
    if time_now > datetime.time(6,30) and time_now < datetime.time(6,40):
        await channel.send(f'It is 6:30am in the UK, and <@{os.getenv("USERID")}> has 15 minutes to wake up.')
        await asyncio.sleep(900)
        if not awake:
            await channel.send(f'<@{os.getenv("USERID")}> Michael did not wake up, streak restarting fs')
            streak = 0
        else:
            streak += 1
            await channel.send(f'<@{os.getenv("USERID")}> has woke up at 5am for {streak} days in a row! Jeez what a pro')
    awake = False
    return

client.run(os.getenv('TOKEN'))

