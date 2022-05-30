
import sqlite3


class Db:
    conn = sqlite3.connect("./database/database.db")
    def query(self,x):
        self.conn.cursor.execute(x)
        self.conn.commit()

    def close(self):
        self.conn.close()