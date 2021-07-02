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

    def get_ids(self):
        result = self.users.find({},{"id":True, "_id":False}) 
        return [user["id"] for user in result]

    def update_current(self, id, current):
        self.users.update_one({"id": id}, {"set": {"timecurrent": current}})

    def increment_streak(self, id):
        user = self.get_user(id)
        self.users.update_one({"id": id}, {"set": {"streak": user["streak"]+1}})

    def reset_streak(self, id):
        self.users.update_one({"id": id}, {"set": {"streak": 0}})

    def get_leaderboard(self):
        return self.users.find({},{"username":True, "streak":True, "timegoal":True,"timezone":True,"_id":False}).sort("streak", -1).limit(10)

    def delete_user(self, id):
        self.users.delete_one({"id": id})

    def get_active_users(self):
        return self.activeusers.find({},{"_id":False})

    def get_active_ids(self):
        result = self.activeusers.find({},{"id":True, "_id":False}) 
        return [user["id"] for user in result]

    def add_to_active(self, id, time):
        self.activeusers.insert_one({"id": id, "time": time})

    def update_active(self, id, time):
        self.activeusers.update_one({"id": id}, {"set": {"time": time}})

    def remove_active(self, id):
        self.activeusers.delete_one({"id": id})

