# Sleep-Bot

A discord bot that tracks sleep and creates habit with gamification.

## Docs

### $setup <timegoal [HH:MM]> <timezone [+/-HH:MM]>   
This is probably the only confusing command. Timegoal represents when you want to wake up in 24 hour time (ie 05:00 would be 5am). Timezone represents your offset relative to UTC. For example, IST is +5.30 ahead of UTC, so the timezone would be +05:30. EST would be -05:00 etc. An example of the full command: **$setup 05:00 +05:30** 

### $up  
As soon as you wake up to reach your goal, you will be 




## Setup  
- venv (optional)
- pip install -r "requirements.txt"
- Fill out env (rename to .env)
- Setup relational db with the following schema (cba setting up the docker, but feel free to do so!):

**users**  
id [text] [PK]  
streak [int] [default=0]  
timezone [real]  
timegoal [text]  
timecurrent [text]  

**activeusers**  
id [text] [PK]  
time [text  

__open to all pull requests!__
