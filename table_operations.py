from tkinter import messagebox


class TableOperations:
    def __init__(self, db):
        self.db = db

    def insert_record(self, values):
        try:
            query = "INSERT INTO STUDENT(NAME, BRANCH, ROLL, SECTION, AGE) VALUES (%s, %s, %s, %s, %s)"
            self.db.cursor.execute(query, values)
            self.db.conn.commit()
            messagebox.showinfo("Success", "Record inserted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not insert record: {e}")

    def update_record(self, values):
        try:
            query = "UPDATE STUDENT SET NAME=%s, BRANCH=%s, SECTION=%s, AGE=%s WHERE ROLL=%s"
            self.db.cursor.execute(query, (values[0], values[1], values[3], values[4], values[2]))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Record updated successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not update record: {e}")

    def delete_record(self, roll_number):
        try:
            query = "DELETE FROM STUDENT WHERE ROLL=%s"
            self.db.cursor.execute(query, (roll_number,))
            self.db.conn.commit()
            messagebox.showinfo("Success", "Record deleted successfully")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete record: {e}")
