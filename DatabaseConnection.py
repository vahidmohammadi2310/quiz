import mysql.connector


class Database:

    def __init__(self, host, user, password, database):
        try:
            self.connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            if self.connection.is_connected():
                print('Successfully connected to database!')
        except Exception as e:
            print(f"While try to connect to database has {e}")
            self.connection = None

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            print('Connection Closed!')
