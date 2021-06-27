# This code ಠ_ಠ fml
import re
import datetime
import discord
from discord.ext import tasks
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()

from dbscript import Connection
connection = Connection()

from timezones import get_time, utc_to_local

get_time("00:40", "CAT")

#connection.new_record("769598266173030470", 0, datetime.time(5,0), "bst")

streak = 0
registered_users = [769598266173030470]
progess_time = datetime.time(13,6)
target_time = datetime.time(5,0)

bot = commands.Bot(command_prefix="$")

def timenow():
    return datetime.datetime.now().time()

@bot.command()
async def up(ctx):
    global progess_time
    global streak
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return
    if str(ctx.message.author.id) not in connection.get_ids():
        await ctx.channel.send(f"{ctx.message.author.mention} You have not set a time, to do so, please say $setup <time>")
        return
    user = connection.get_user(str(ctx.message.author.id))
    if timenow() <= target_time and timenow() >= (target_time - datetime.delta(minutes=15)):
        await ctx.channel.send(f"{ctx.message.author.mention} Congrats, you have kept your time goal for {streak} days!")
        progess_time = target_time
        streak += 1
        return
    if timenow() > progess_time:
        await ctx.channel.send(f"{ctx.message.author.mention} Your missed your target of {progess_time}, your new target is {timenow()}")
        progess_time = timenow()
    elif timenow() <= progess_time and timenow() > target_time:
        await ctx.channel.send(f"{ctx.message.author.mention} Congrats, you beat your target time of {progess_time}, your new target is {timenow()}")
        progess_time = timenow()
    else:
        await ctx.channel.send(f"You have woken up for your target goal of {target_time} too early. Either that or the bot is bugged idk.")
    streak = 0
    return

@bot.command()
async def setup(ctx, goal, timezone):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return
    if str(ctx.message.author.id) in connection.get_ids():
        await ctx.channel.send(f"{ctx.message.author.mention} You have already setup your sleeping. To reset, use $reset (this will reset your streak as well).")
    elif goal is None or timezone is None:
        await ctx.channel.send(f"{ctx.message.author.mention} Please input parameters, the command should look like this $setup <timegoal> <timezone>")
    elif not re.match(r"[0-9][0-9]:[0-9][0-9]", goal):
        await ctx.channel.send(f"{ctx.message.author.mention} Time format does not match, please use HH:MM (for example 05:00 is 5am)")
    elif isinstance(timezone, str):
        timezone = timezone.upper()
        format_time = get_time(goal, timezone)
        if format_time is None:
            await ctx.channel.send(f"{ctx.message.author.mention} Your timezone is not valid, please use a timezone such as BST")
            return
        connection.new_record(str(ctx.message.author.id), 0, format_time, timezone)
        await ctx.channel.send(f"{ctx.message.author.mention} Your time has been set!")
    return

@bot.command()
async def reset(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return
    if str(ctx.message.author.id) not in connection.get_ids():
        await ctx.channel.send(f"{ctx.message.author.mention} You are not found in the database, to setup please say $setup <timegoal> <timezone>")
        return
    connection.delete_user(str(ctx.message.author.id))
    await ctx.channel.send(f"{ctx.message.author.mention} Reset user, please now use $setup")

@bot.command()
async def leaderboard(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return
    text = f"{ctx.message.author.mention} Top active streaks:\n\n"
    leaderboard = connection.get_leaderboard()
    for user in leaderboard:
        username = await bot.fetch_user(int(user[0]))
        text += f"{username}: {user[1]} days\n"
    await ctx.channel.send(f"{text}")

@bot.command()
async def mystats(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return
    if str(ctx.message.author.id) not in connection.get_ids():
        await ctx.channel.send(f"{ctx.message.author.mention} You are not found in the database, to setup please say $setup <timegoal> <timezone>")
        return
    user = connection.get_user(str(ctx.message.author.id))
    text = f"{ctx.message.author.mention} Goal: {utc_to_local(user[3], user[2])}, current wake up time: {utc_to_local(user[4], user[2])}, current streak: {user[1]} ({user[2]})"
    await ctx.channel.send(text)

@tasks.loop(seconds=60)
async def get_active_times():
    return

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    get_active_times.start()

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

