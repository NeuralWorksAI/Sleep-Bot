# Sleep-Bot

A discord bot that tracks sleep and creates habit with gamification.

## Docs

### $setup <timegoal [HH:MM]> <timezone [+/-HH:MM]>

This is probably the only confusing command. Timegoal represents when you want to wake up in 24 hour time (ie 05:00 would be 5am). Timezone represents your offset relative to UTC. For example, IST is +5.30 ahead of UTC, so the timezone would be +05:30. EST would be -05:00 etc. An example of the full command: **$setup 05:00 +05:30**

### $reset

Resets your goal, This will also remove your streak. Once you have reset you will need to use $setup again.

### $leaderboard

View the leaderboard ranked by longest active streak.

### $mystats

View your stats including current streak, current goal, target goal and timezone.

### $site

View a live version of the leaderboards, along with help on: [NeuralWorks Sleep Bot Site](https://neuralworks.group/Sleep-Bot/)

## Setup

- venv (optional)
- pip install -r "requirements.txt"
- Setup mongoDb
- Fill out env (rename to .env)

**open to all pull requests!**
