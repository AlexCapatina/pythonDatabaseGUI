import mysql.connector


class Database:
    def __init__(self, user, password, database):
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to database successfully")

            self.cursor = self.connection.cursor()
        except mysql.connector.Error as error:
            print(f"Error connecting to database: {error}")
            self.connection = None
            self.cursor = None

    def get_databases(self):
        if not self.connection:
            return []

        # cursor = self.connection.cursor()
        self.cursor.execute("SHOW DATABASES")
        return [db[0] for db in self.cursor.fetchall()]