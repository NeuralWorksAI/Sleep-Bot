# Sleep-Bot

A discord bot that tracks sleep and creates habit with gamification.

## Docs

### $setup <goal> 


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
