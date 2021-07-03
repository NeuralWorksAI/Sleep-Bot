from datetime import datetime, timedelta
import pymongo
import os

class Connection():
    def __init__(self):
        print("initiating db")
        self.client = pymongo.MongoClient(os.getenv("MONGOURI"))
        self.sleepdb = self.client["Main"]
        self.users = self.sleepdb["users"]
        self.activeusers = self.sleepdb["activeusers"]

    def new_record(self, name, streak, timezone, time_goal, username):
        self.users.insert_one({"id": name, "streak": streak, "timezone": timezone, "timegoal": time_goal, "timecurrent": time_goal, "username": username})

    def get_user(self, id):
        return self.users.find_one({"id": id}, {"_id":0})

    def get_users(self):
        return self.users.find({},{"_id":0})

    def get_ids(self):
        result = self.users.find({},{"id":1, "_id":0}) 
        return [user["id"] for user in result]

    def update_current(self, id, current):
        current += timedelta(days=1)
        self.users.update_one({"id": id}, {"$set": {"timecurrent": str(current)}})

    def update_goal(self, id, goal):
        goal += timedelta(days=1)
        self.users.update_one({"id": id}, {"$set": {"timegoal": str(goal)}})

    def increment_streak(self, id):
        user = self.get_user(id)
        self.users.update_one({"id": id}, {"$set": {"streak": user["streak"]+1}})

    def reset_streak(self, id):
        self.users.update_one({"id": id}, {"$set": {"streak": 0}})

    def get_leaderboard(self):
        return self.users.find({},{"username":1, "streak":1, "timegoal":1,"timezone":1,"_id":0}).sort("streak", -1).limit(10)

    def delete_user(self, id):
        self.users.delete_one({"id": id})


