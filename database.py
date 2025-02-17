import mysql.connector
from tkinter import messagebox


class Database:
    def __init__(self, user, password, database):
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user=user,
                password=password,
                database=database
            )
            self.cursor = self.conn.cursor()
            print("Connected to database successfully!")
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Database connection failed: {error}")

    def get_databases(self, user, password):
        try:
            temp_conn = mysql.connector.connect(
                host="localhost",
                user=user,
                password=password
            )
            temp_cursor = temp_conn.cursor()
            temp_cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in temp_cursor.fetchall()]
            temp_conn.close()
            return databases
        except mysql.connector.Error as error:
            messagebox.showerror("Error", f"Could not fetch databases: {error}")
            return[]

    def close(self):
        self.conn.close()
