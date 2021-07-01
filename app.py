from flask import Flask, render_template
from dbscript import Connection
from timezones import utc_to_local


app = Flask(__name__)

def dtstring(time):
    newtime = str(time).split(":")
    return newtime[0]+":"+newtime[1]

@app.route("/")
def index():
    connection = Connection()
    data = []
    raw_data = connection.get_leaderboard()
    for user in raw_data:
        time = utc_to_local(user["timegoal"], user["timezone"])
        data.append([user["username"], user["streak"], dtstring(time)])
    return render_template("index.html", leaderboard=data)

@app.route("/help")
def help():
    return render_template("help.html")