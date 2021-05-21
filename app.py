import datetime
import discord
from discord.ext import tasks
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents().all()
awake = False
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_member_update(before, after):
    global awake
    if awake:
        return
    if after.id == int(os.getenv('USERID')):
        print('Michael is online')
        awake = True
        print(awake)

@tasks.loop(seconds=10)
async def is_awake():
    global awake
    time_now = datetime.datetime.now().time()
    if time_now > datetime.time(4,55) and time_now < datetime.time(5,0):
        print(awake)
        await asyncio.sleep(900)
        print(awake)
        if not awake:
            print("you are not awake")
        else:
            print("awake")
    awake = False
    return

is_awake.start()

client.run(os.getenv('TOKEN'))