import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
from table_operations import TableOperations


class pythonDB:
    def __init__(self, root):
        self.root = root
        self.root.title("Student records")
        self.root.geometry("800x600")

        self.database = None
        self.student_ops = None

        # User and password inputs
        tk.Label(root, text="Username: ").pack()
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password: ").pack()
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        # Database drop down manu
        tk.Label(root, text="Select database: ").pack()
        self.database_var = tk.StringVar()
        self.database_dropdown = ttk.Combobox(root, textvariable=self.database_var, state="readonly")
        self.database_dropdown.pack()

        self.return_database_button = tk.Button(root, text="Return database", command=self.load_database)
        self.return_database_button.pack()

        # Display table
        self.tree = ttk.Treeview(root)
        self.tree.pack(expand=True, fill="both")

        # CRUD buttons
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Insert", command=self.insert_record, width=12).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Update", command=self.update_record, width=12).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Delete", command=self.delete_record, width=12).grid(row=0, column=2, padx=5)

    def load_database(self):
        if not self.username_entry.get() or not self.password_entry.get():
            messagebox.showerror("Error", "Please enter username and password first")
            return

        db_temp = Database(self.username_entry.get(), self.password_entry.get(), "")
        databases = db_temp.get_databases()

        if databases:
            self.database_dropdown["values"] = databases
        else:
            messagebox.showerror("Error", "No databases found or incorrect credentials!")

        return_database_button = tk.Button(root, text="Return databases", command=self.load_database)
        return_database_button.pack()

    def connect_database(self):
        self.database = Database(self.username_entry.get(), self.password_entry.get(), self.database_var.get())
        self.student_ops = TableOperations(self.database)
        messagebox.showinfo("Success", "Connected to database successfully")

    def insert_record(self):
        values = ["John", "CS", "101", "A", "20"]
        self.student_ops.insert_record(values)

    def update_record(self):
        values = ["John Doe", "IT", "101", "B", "21"]
        self.student_ops.update_record(values)

    def delete_record(self):
        roll_number = "101"
        self.student_ops.delete_record(roll_number)


if __name__ == "__main__":
    root = tk.Tk()
    app = pythonDB(root)
    root.mainloop()
