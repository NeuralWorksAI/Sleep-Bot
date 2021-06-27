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

    def get_leaderboard(self):
        self.cur.execute("SELECT id, streak FROM users ORDER BY streak DESC")
        return [item for item in self.cur.fetchmany(10)]

    def delete_user(self, id):
        self.cur.execute("DELETE FROM users WHERE id = %s", (id,))
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()


