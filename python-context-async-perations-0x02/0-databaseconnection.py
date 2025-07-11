import sqlite3

class DatabaseConnection:
    def __init__(self, database_name):
        self.db_name = database_name

    def __enter__(self):
        self.conn = sqlite3.connect(self.database_name)
        return self.conn  

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

with DatabaseConnection("sampleDb.sqlite") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    results = cursor.fetchall()
    print(results)
