# This code ಠ_ಠ fml
import re
from datetime import datetime, timedelta
from discord.ext import tasks
from discord.ext import commands
from discord import Intents
import os
from dotenv import load_dotenv
load_dotenv()

from dbscript import Connection
connection = Connection()

from timezones import utc_to_local, dtstring

intents = Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)

#Tasks
@tasks.loop(hours=48)
async def remove_inactive_users():
    if remove_inactive_users.current_loop != 0:
        channel = bot.get_channel(int(os.getenv("CHANNELID")))
        active_list = connection.get_users()
        for user in active_list:
            user_time = user["timegoal"]
            if datetime.utcnow() > datetime.strptime(user_time, '%Y-%m-%d %H:%M:%S.%f'):
                await channel.send(f"<@{user['id']}> You have not been active on discord for a while. Reseting streak.")
                connection.delete_user(user['id'])

@bot.event
async def on_member_update(before, after):
    if str(before.status) == "offline" and str(before.id) in connection.get_ids() and str(before.id):
        strid = str(before.id)
        user = connection.get_user(strid)
        time = datetime.strptime(user["timegoal"], '%Y-%m-%d %H:%M:%S.%f')
        current_time = datetime.strptime(user["timecurrent"], '%Y-%m-%d %H:%M:%S.%f')
        time_local = utc_to_local(time, user["timezone"])
        current_time_local = utc_to_local(current_time, user["timezone"])
        if datetime.utcnow() > (time - timedelta(hours=3)):
            channel = bot.get_channel(int(os.getenv("CHANNELID")))
            if datetime.utcnow() >= (time - timedelta(hours=3)) and datetime.utcnow() < (time - timedelta(minutes=15)):
                await channel.send(f"<@{strid}> You have woken up for your target goal of {dtstring(time_local)} too early")
                connection.update_current(strid, current_time)

            elif datetime.utcnow() >= (time - timedelta(minutes=15)) and datetime.utcnow() <= (time + timedelta(minutes=15)):
                await channel.send(f"<@{strid}> Congrats, you have kept your time goal for {user['streak']+1} days!")
                connection.update_current(strid, time)
                connection.update_goal(strid, time)
                connection.increment_streak(strid)
                return

            elif datetime.utcnow() <= current_time and datetime.utcnow() > time:
                new_current = datetime.utcnow() - timedelta(minutes=15)
                await channel.send(f"<@{strid}> Congrats, you beat your target time of {dtstring(current_time_local)}, your new target is {dtstring(utc_to_local(new_current, user['timezone']))}")
                connection.update_current(strid, new_current)

            elif datetime.utcnow() > current_time:
                await channel.send(f"<@{strid}> You missed your target of {dtstring(current_time_local)}, your new target is {dtstring(utc_to_local(datetime.utcnow(), user['timezone']))}")
                connection.update_current(strid, datetime.utcnow())

            connection.update_goal(strid, time)
            connection.reset_streak(strid)

@bot.command()
async def setup(ctx, goal=None, timezone=None):
    if ctx.channel.id != int(os.getenv('CHANNELID')): #If wrong channel
        return

    if str(ctx.message.author.id) in connection.get_ids(): #If user is already setup
        await ctx.channel.send(f"{ctx.message.author.mention} You have already setup your sleeping. To reset, use $reset (this will reset your streak as well).")
    
    elif goal == None or timezone == None: #If nothing entered
        await ctx.channel.send(f"{ctx.message.author.mention} Please input parameters, the command should look like this $setup <timegoal HH:MM> <timezone (relative to UTC) [+-]HH:MM>")
    
    elif not re.match(r"[0-9][0-9]:[0-9][0-9]", goal): #If goal regex does not match 
        await ctx.channel.send(f"{ctx.message.author.mention} Time format does not match, please use HH:MM (for example 05:00 is 5am)")
    
    elif isinstance(timezone, str):
        if not re.match(r"[+-][0-9][0-9]:[0-9][0-9]", timezone): #If timezone regex does not match
            await ctx.channel.send(f"{ctx.message.author.mention} Your timezone is not valid, please use the timezone format (relative to UTC) [+-]HH:MM")
            return
        
        sign = timezone[0]
        timezone = int(timezone[1:3])*60 + (int(timezone[4:6]))
        if sign == "-":
            timezone = 0 - timezone
        user_datetime = datetime.utcnow().replace(hour=int(goal[0:2]), minute=int(goal[3:5]))
        user_utc_time = user_datetime + timedelta(days=1)
        user_utc_time -= timedelta(minutes=timezone)
        username = await bot.fetch_user(int(ctx.message.author.id))
        username = str(username)
        connection.new_record(str(ctx.message.author.id), 0, timezone, str(user_utc_time),  username)
        await ctx.channel.send(f"{ctx.message.author.mention} Your time has been set!")
    return


@bot.command()
async def reset(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return

    strid = str(ctx.message.author.id)
    if strid not in connection.get_ids():
        await ctx.channel.send(f"{ctx.message.author.mention} You are not found in the database, to setup please say $setup <timegoal> <timezone>")
        return

    connection.delete_user(strid)
    await ctx.channel.send(f"{ctx.message.author.mention} Reset user, please now use $setup")


@bot.command()
async def leaderboard(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return

    text = f"{ctx.message.author.mention} Top active streaks:\n"
    leaderboard = connection.get_leaderboard()
    for user in leaderboard:
        text += f"{user['username']}: {user['streak']} days\n"
    await ctx.channel.send(f"{text}")


@bot.command()
async def mystats(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return

    if str(ctx.message.author.id) not in connection.get_ids():
        await ctx.channel.send(f"{ctx.message.author.mention} You are not found in the database, to setup please say $setup <timegoal> <timezone>")
        return

    user = connection.get_user(str(ctx.message.author.id))
    goal = utc_to_local(user['timegoal'], user['timezone'])
    current = utc_to_local(user['timecurrent'], user['timezone'])
    text = f"{ctx.message.author.mention} Goal: {dtstring(goal)}, current wake up time: {dtstring(current)}, current streak: {user['streak']} (timezone: {user['timezone']})"
    await ctx.channel.send(text)


@bot.command()
async def site(ctx):
    if ctx.channel.id != int(os.getenv('CHANNELID')):
        return

    await ctx.channel.send(f"{ctx.message.author.mention} View the live leaderboards: **https://nw-sleep-bot.herokuapp.com/**")

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user.name}')
    remove_inactive_users.start()

bot.run(os.getenv('TOKEN'))

