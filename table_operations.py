from tkinter import messagebox
import mysql.connector


class TableOperations:
    def __init__(self, database):
        self.database = database
        self.cursor = self.database.connection.cursor()

    def get_table_data(self):
        try:
            self.cursor.execute("SELECT * FROM STUDENT")
            rows = self.cursor.fetchall()

            self.cursor.execute("SHOW COLUMNS FROM STUDENT")
            columns = [col[0] for col in self.cursor.fetchall()]
            return rows, columns

        except mysql.connector.Error as error:
            print(f"Error fetching table: {error}")
            return [], []

    def insert_record(self, values):
        try:
            queryInsert = "INSERT INTO STUDENT(NAME, BRANCH, ROLL, SECTION, AGE) VALUES (%s, %s, %s, %s, %s)"
            self.cursor.execute(queryInsert, values)
            self.database.connection.commit()
            messagebox.showinfo("Success", "Record inserted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not insert record: {e}")

    def update_record(self, values):
        try:
            queryUpdate = "UPDATE STUDENT SET NAME=%s, BRANCH=%s, SECTION=%s, AGE=%s WHERE ROLL=%s"
            self.cursor.execute(queryUpdate, (values[0], values[1], values[3], values[4], values[2]))
            self.database.connection.commit()
            messagebox.showinfo("Success", "Record updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update record: {e}")

    def delete_record(self, roll_number):
        try:
            queryDelete = "DELETE FROM STUDENT WHERE ROLL=%s"
            self.cursor.execute(queryDelete, (roll_number,))
            self.database.connection.commit()
            messagebox.showinfo("Success", "Record deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete record: {e}")
