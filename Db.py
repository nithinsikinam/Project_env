import sqlite3

class Db:
    conn = sqlite3.connect("./database/database.db")
    def setter(self,x):
        self.conn.execute(x)
        self.conn.commit()
    
    def getter(self,x):
        c=self.conn.execute(x)
        return c   

    def close(self):
        self.conn.close()

   