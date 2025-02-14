import subprocess
import mysql.connector
import time
import tkinter as tk
from tkinter import ttk, messagebox
from flask import Flask, request, jsonify

schoolApp = Flask(__name__)


def is_mysql_running():
    mysql_status = subprocess.run("net start | findstr /I 'MySQL'", shell=True, capture_output=True, text=True)
    return "MySQL" in mysql_status.stdout


# if not is_mysql_running():
#     print("Starting database!")
#     subprocess.run("net start MySQL84", shell=True)
#     time.sleep(3)
# else:
#     print("MySQL is already running")

def get_databases():
    try:
        temp_conn = mysql.connector.connect(
            host="localhost",
            user=username_entry.get(),
            password=password_entry.get()
        )
        temp_cursor = temp_conn.cursor()
        temp_cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in temp_cursor.fetchall()]
        temp_conn.close()
        return databases
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Could not fetch databases: {error}")


# Connect to the database
def connect_database():
    global dataBase, cursorObject

    try:
        dataBase = mysql.connector.connect(
            host="localhost",
            user=username_entry.get(),
            password=password_entry.get()
            , database=database_var.get()
        )
        cursorObject = dataBase.cursor()
        messagebox.showinfo("Success", "Connected to teh database successfully")
        load_table()
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Could not connect to database: {error}")

# cursorObject = dataBase.cursor()

# Grab data from the STUDENT table
def load_table():
    cursorObject.execute("SELECT * FROM STUDENT")
    rows = cursorObject.fetchall()
    cursorObject.execute("SHOW COLUMNS FROM STUDENT")
    columns = [col[0] for col in cursorObject.fetchall()]

    tree["columns"] = columns
    tree["show"] = "headings"

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    # Clear previous data
    for item in tree.get_children():
        tree.delete(item)

    # Insert data into Treeview
    for row in rows:
        tree.insert("", "end", values=row)


# # Create the database if it doesn't exist
# cursorObject.execute("CREATE DATABASE IF NOT EXISTS testPython_db")

# #Create table
# studentRecord = """CREATE TABLE IF NOT EXISTS STUDENT (
#                    NAME  VARCHAR(20) NOT NULL,
#                    BRANCH VARCHAR(50),
#                    ROLL INT NOT NULL,
#                    SECTION VARCHAR(5),
#                    AGE INT
#                    ) """
# cursorObject.execute(studentRecord)
#
# # Show table in the database
# cursorObject.execute("SHOW TABLES")
# print("Connection established")
# print("\nTables in the database:")
# for table in cursorObject:
#     print(table[0]) # This will print the table name
#
# # Describe the STUDENT table structure
# cursorObject.execute("DESCRIBE STUDENT")
# print("\nTable Structure:")
# for column in cursorObject:
#     print(column)

# dataBase.close()

# Create window with Tkinter
root = tk.Tk()
root.title("Student Records")
root.geometry("800x600")

# MySQL user and password inputs
tk.Label(root, text="Username: ").pack()
username_entry = tk.Entry(root)
username_entry.pack()

tk.Label(root, text="Password: ").pack()
password_entry = tk.Entry(root, show="*")
password_entry.pack()

# Database dropdown menu
tk.Label(root, text="Select database: ").pack()
database_var = tk.StringVar()
database_dropdown = ttk.Combobox(root, textvariable=database_var, state="readonly")
database_dropdown.pack()

return_database_button = tk.Button(root, text="Return databases", command=lambda: database_dropdown.config(values = get_databases()))
return_database_button.pack()

connect_btn = tk.Button(root, text="Connect to database", command=connect_database)
connect_btn.pack()

tree = ttk.Treeview(root)
tree.pack(expand=True, fill="both")

frame = tk.Frame(root)
frame.pack(pady=10)

labels = ["Name", "Branch", "Roll", "Section", "Age"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(frame, text=label).grid(row=0, column=i)
    entry = tk.Entry(frame, width=12)
    entry.grid(row=1, column=i)
    entries[label] = entry


def insertRecord():
    values = [entries[label].get() for label in labels]
    if not values[2].isdigit():
        messagebox.showerror("Error", "Roll number must be a valid integer")
        return

    try:
        cursorObject.execute("INSERT INTO STUDENT(NAME, BRANCH, ROLL, SECTION, AGE) VALUES (%s, %s, %s, %s, %s)",
                             values)
        dataBase.commit()
        tree.insert("", "end", values=values)
        messagebox.showinfo("Success", "Record inserted successfully!")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Could not insert record: {error}")


def updateRecord():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a record to update.")
        return

    values = [entries[label].get() for label in labels]
    if not values[2].isdigit():
        messagebox.showerror("Error", "Roll number must be a valid integer.")
        return
    values[2] = int(values[2])

    try:
        cursorObject.execute("UPDATE STUDENT SET NAME=%s, BRANCH=%s, SECTION=%s, AGE=%s WHERE ROLL=%s",
                             (values[0], values[1], values[3], values[4], values[2]))
        dataBase.commit()
        tree.item(selected_item, values=values)
        messagebox.showinfo("Success", "Record updated successfully")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Could not update record: {error}")


def delete_record():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Select a record to delete")
        return

    values = tree.item(selected_item, "values")
    roll_number = values[2]

    try:
        cursorObject.execute("DELETE FROM STUDENT WHERE ROLL=%s", (roll_number,))
        dataBase.commit()
        tree.delete(selected_item)
        messagebox.showinfo("Success", "Record deleted successfullY!")
    except mysql.connector.Error as error:
        messagebox.showerror("Error", f"Could not delete record: {error}")


# Buttons
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Insert", command=insertRecord, width=12).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Update", command=updateRecord, width=12).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Delete", command=delete_record, width=12).grid(row=0, column=2, padx=5)

root.mainloop()
