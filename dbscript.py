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
        self.cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s)", (name, streak, time_goal, timezone))
        print("Added new record")
        self.conn.commit()

    def get_all(self):
        self.cur.execute("SELECT * FROM users")
        records = self.cur.fetchall()
        print(records)

    def get_ids(self):
        self.cur.execute("SELECT id FROM users")
        records = self.cur.fetchall()
        print(records)

    def close_connection(self):
        self.cur.close()
        self.conn.close()
        print("Connection closed")


