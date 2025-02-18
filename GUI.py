import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from table_operations import TableOperations


class pythonDB(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student records")
        self.geometry("1000x600")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        for Frs in (LoginWindow, DatabaseSelectionWindow, tableScreen):
            frame = Frs(self.container, self)
            self.frames[Frs] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(LoginWindow)

    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

        # self.database = None
        # self.student_ops = None


class LoginWindow(tk.Frame):
    def __init__(self, mainFrame, controller):
        super().__init__(mainFrame)
        self.controller = controller

        tk.Label(self, text="Username: ").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password: ").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.login).pack()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username and password:
            self.controller.username = username
            self.controller.password = password
            self.controller.show_frame(DatabaseSelectionWindow)
        else:
            messagebox.showerror("Error", "Please enter both username and password")


class DatabaseSelectionWindow(tk.Frame):
    def __init__(self, mainFrame, controller):
        super().__init__(mainFrame)
        self.controller = controller

        # Database drop down manu
        tk.Label(self, text="Select database: ").pack()
        self.database_var = tk.StringVar()
        self.database_dropdown = ttk.Combobox(self, textvariable=self.database_var, state="readonly")
        self.database_dropdown.pack()

        self.return_database_button = tk.Button(self, text="Return database", command=self.load_database)
        self.return_database_button.pack()

        self.connectButton = tk.Button(self, text="Connect", command=self.connect_database)
        self.connectButton.pack()

        # Display table
        # self.tree = ttk.Treeview(self)
        # self.tree.pack(expand=True, fill="both")

    def load_database(self):
        temporaryDB = Database(self.controller.username, self.controller.password, "")
        databases = temporaryDB.get_databases()

        if databases:
            self.database_dropdown["values"] = databases
        else:
            messagebox.showerror("Error", "No databases elected or wrong login credentials")

        # if not self.database_var.get():
        #     messagebox.showerror("Error", "Please select a database first")
        #     return

        # self.database = Database(self.username_entry.get(), self.password_entry.get(), self.database_var.get())
        # self.student_ops = TableOperations(self.database)
        # messagebox.showinfo("Success", f"Connected to {self.database_var.get()} successfully")
        #
        # # self.load_database()
        # self.load_table()

    def connect_database(self):
        selectedDB = self.database_var.get()
        if not selectedDB:
            messagebox.showerror("Error", "Database not selected. Please select a database and then you can continue.")
            return
        self.controller.database = Database(self.controller.username, self.controller.password, selectedDB)
        self.controller.tableOperations = TableOperations(self.controller.database)

        messagebox.showinfo("Success", f"You are now connected to {selectedDB}")

        tableWindow = self.controller.frames[tableScreen]
        tableWindow.load_table()

        self.controller.show_frame(tableScreen)


class tableScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.tree = ttk.Treeview(self)
        self.tree.pack(expand=True, fill="both")

        frameButton = tk.Frame(self)
        frameButton.pack(pady=10)

        tk.Button(frameButton, text="Insert", command=self.insert_record, width=12).grid(row=0, column=0, padx=5)
        tk.Button(frameButton, text="Update", command=self.update_record, width=12).grid(row=0, column=1, padx=5)
        tk.Button(frameButton, text="Delete", command=self.delete_record, width=12).grid(row=0, column=2, padx=5)

        # CRUD buttons
        self.entries = {}
        labels = ["Name", "Branch", "Roll", "Section", "Age"]
        inputBox = tk.Frame(self)
        inputBox.pack(pady=10)

        for i, labels in enumerate(labels):
            tk.Label(inputBox, text=labels).grid(row=0, column=i)
            entry = tk.Entry(inputBox, width=12)
            entry.grid(row=1, column=i)
            self.entries[labels] = entry

        # self.load_table()
        # if not self.username_entry.get() or not self.password_entry.get():
        #     messagebox.showerror("Error", "Please enter username and password first")
        #     return
        #
        # db_temp = Database(self.username_entry.get(), self.password_entry.get(), "")
        # databases = db_temp.get_databases()
        #
        # if databases:
        #     self.database_dropdown["values"] = databases
        # else:
        #     messagebox.showerror("Error", "No databases found or incorrect credentials!")
        #
        # if not hasattr(self, "return_database_button"):
        #     return_database_button = tk.Button(self.root, text="Return databases", command=self.load_database)
        #     return_database_button.pack()
        #
        # if not hasattr(self, "connect_button"):
        #     self.connect_button = tk.Button(self.root, text="Connect to Database", command=self.connect_database)
        #     self.connect_button.pack()

    def load_table(self):
        rows, columns = self.controller.tableOperations.get_table_data()
        self.tree["columns"] = columns
        self.tree["show"] = "headings"

        if not self.controller.tableOperations:
            messagebox.showerror("Error", "Not connected to any database")
            return

        if not rows:
            messagebox.showwarning("Warning", "No records found in STUDENT table")
            return

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in rows:
            self.tree.insert("", "end", values=row)

    def insert_record(self):
        values = [self.entries[label].get() for label in ["Name", "Branch", "Roll", "Section", "Age"]]
        if not values[2].isdigit():
            messagebox.showerror("Error", "Roll number must be a valid integer.")
            return
        values[2] = int(values[2])
        self.controller.tableOperations.insert_record(values)

        self.load_table()

    def update_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select record to update")
            return

        values = [self.entries[label].get() for label in ["Name", "Branch", "Roll", "Section", "Age"]]
        if not values[2].isdigit():
            messagebox.showerror("Error", "Roll number must be a valid integer.")
            return

        self.controller.tableOperations.update_record(values)

        self.load_table()

    def delete_record(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select record to delete")
            return

        values = self.tree.item(selected_item, "values")
        roll_number = values[2]

        self.controller.tableOperations.delete_record(roll_number)
        self.load_table()
