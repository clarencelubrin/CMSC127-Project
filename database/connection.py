import mariadb
import sys

class DBConnection:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(
        self,
        user="root",
        password="password",
        host="localhost",
        port=3306,
        database="mydatabase"
    ):
        # Connect to MariaDB 
        try:
            self.conn = mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=database
            )
            print("Successfully connected to MariaDB Platform")
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor object
        self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def commit(self):
        if self.conn:
            self.conn.commit()  