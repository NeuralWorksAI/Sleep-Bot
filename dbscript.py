import psycopg2
import os

class Connection():
    def __init__(self):
        self.conn = psycopg2.connect(
            host = os.getenv('HOST'), #If you are running locally this will probably be "localhost"
            database = os.getenv('DATABASE'),
            user=os.getenv('POSTGRES_USERNAME'),
            password=os.getenv('POSTGRES_PASSWORD')
            )
        self.cur = self.conn.cursor()

    def new_record(self, name, streak, time_goal, timezone):
        self.cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s)", (name, streak, timezone, time_goal, time_goal))
        self.conn.commit()

    def get_user(self, id):
        self.cur.execute("SELECT * FROM users WHERE id = %s", (id,))
        return [item for item in self.cur.fetchone()]

    def get_ids(self):
        self.cur.execute("SELECT id FROM users")
        return [item[0] for item in self.cur.fetchall()]

    def update_current(self, id, current):
        self.cur.execute("UPDATE users SET timecurrent = %s WHERE id = %s", (current,id))
        self.conn.commit()

    def increment_streak(self, id):
        user = self.get_user(id)
        print(user)
        self.cur.execute("UPDATE users SET streak = %s WHERE id = %s", (int(user[1])+1,id))
        self.conn.commit()

    def reset_streak(self, id):
        self.cur.execute("UPDATE users SET streak = 0 WHERE id = %s", (id,))
        self.conn.commit()

    def get_leaderboard(self):
        self.cur.execute("SELECT id, streak FROM users ORDER BY streak DESC")
        return [item for item in self.cur.fetchmany(10)]

    def delete_user(self, id):
        self.cur.execute("DELETE FROM users WHERE id = %s", (id,))
        self.conn.commit()

    def get_active_users(self):
        self.cur.execute("SELECT * FROM activeusers")
        return [item for item in self.cur.fetchall()]

    def get_active_ids(self):
        self.cur.execute("SELECT id FROM activeusers")
        return [item[0] for item in self.cur.fetchall()]

    def add_to_active(self, id, time):
        self.cur.execute("INSERT INTO activeusers VALUES (%s, %s)", (id, time))
        self.conn.commit()

    def update_active(self, id, time):
        self.cur.execute("UPDATE activeusers SET time = %s WHERE id = %s", (time,id))
        self.conn.commit()

    def remove_active(self, id):
        self.cur.execute("DELETE FROM activeusers WHERE id = %s", (id,))
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()


