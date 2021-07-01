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
        #self.cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s)", (name, streak, timezone, time_goal, time_goal, username))
        self.users.insert_one({"id": name, "streak": streak, "timezone": timezone, "timegoal": time_goal, "timecurrent": time_goal, "username": username})

    def get_user(self, id):
        #self.cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        user = self.users.find_one({"id": id}, {"_id":0})
        return user

    def get_ids(self):
        #self.cur.execute("SELECT id FROM users")
        result = self.users.find({},{"id":True, "_id":False}) 
        return [user["id"] for user in result]

    def update_current(self, id, current):
        #self.cur.execute("UPDATE users SET timecurrent = %s WHERE id = %s", (current,id))
        self.users.update_one({"id": id}, {"set": {"timecurrent": current}})

    def increment_streak(self, id):
        #self.cur.execute("UPDATE users SET streak = %s WHERE id = %s", (int(user[1])+1,id))
        user = self.get_user(id)
        self.users.update_one({"id": id}, {"set": {"streak": user[1]+1}})

    def reset_streak(self, id):
        #self.cur.execute("UPDATE users SET streak = 0 WHERE id = %s", (id,))
        self.users.update_one({"id": id}, {"set": {"streak": 0}})

    def get_leaderboard(self):
        #self.cur.execute("SELECT username, streak, timegoal, timezone FROM users ORDER BY streak DESC")
        return self.users.find({},{"username":True, "streak":True, "timegoal":True,"timezone":True,"_id":False}).sort("streak", -1).limit(10)


    def delete_user(self, id):
        #self.cur.execute("DELETE FROM users WHERE id = %s", (id,))
        self.users.delete_one({"id": id})

    def get_active_users(self):
        #self.cur.execute("SELECT * FROM activeusers")
        return self.activeusers.find({},{"_id":False})

    def get_active_ids(self):
        #self.cur.execute("SELECT id FROM activeusers")
        result = self.activeusers.find({},{"id":True, "_id":False}) 
        return [user["id"] for user in result]

    def add_to_active(self, id, time):
        #self.cur.execute("INSERT INTO activeusers VALUES (%s, %s)", (id, time))
        self.activeusers.insert_one({"id": id, "time": time})

    def update_active(self, id, time):
        #self.cur.execute("UPDATE activeusers SET time = %s WHERE id = %s", (time,id))
        self.activeusers.update_one({"id": id}, {"set": {"time": time}})

    def remove_active(self, id):
        #self.cur.execute("DELETE FROM activeusers WHERE id = %s", (id,))
        self.activeusers.delete_one({"id": id})

