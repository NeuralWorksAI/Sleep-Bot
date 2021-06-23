# This code ಠ_ಠ fml

import datetime
import discord
from discord.ext import tasks
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

# intents = discord.Intents().all()
# awake = False
# streak = 0
# client = discord.Client(intents=intents)
target_time = datetime.time(5,0)
bot = commands.Bot(command_prefix="$")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    # is_awake.start()

@bot.command()
async def up(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return
    if datetime.datetime.now().time() > target_time:
        pass
    await ctx.channel.send("hello")

# @tasks.loop(seconds=60)
# async def is_awake():
#     global awake
#     global streak

#     channel = client.get_channel(int(os.getenv('CHANNELID')))  # notification channel
#     time_now = datetime.datetime.now().time()
#     if time_now > datetime.time(4,25) and time_now < datetime.time(4,35):
#         await channel.send(f'It is 5:30am in the UK, and <@{os.getenv("USERID")}> has 15 minutes to wake up.')
#         await asyncio.sleep(900)
#         if not awake:
#             await channel.send(f'<@{os.getenv("USERID")}> Michael did not wake up, streak restarting')
#             streak = 0
#         else:
#             streak += 1
#             await channel.send(f'<@{os.getenv("USERID")}> has woke up at 5am for {streak} days in a row! Jeez what a pro')
#     time_now = datetime.datetime.now().time()
#     awake = False
#     return

bot.run(os.getenv('TOKEN'))
# client.run(os.getenv('TOKEN'))

