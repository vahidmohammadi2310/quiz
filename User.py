from tkinter import messagebox
from datetime import date


class User:
    def __init__(self, db_connection):
        self.connection = db_connection

    def user_list(self):
        try:
            query = """
                select users.full_name, users.phone, users.age, users.register_date, roles.title as role
                from users
                left join roles
                    on users.role_id = roles.id
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch question: {e}")
        finally:
            cursor.close()

    def create_new_user(self, full_name, phone, password, age=None):
        try:
            query = """
                insert into users (full_name, role_id, phone, password, age, register_date)
                values (%s,%s,%s,%s,%s,%s)
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (full_name, 2, phone, password, age, date.today()))
            self.connection.commit()
            messagebox.showinfo("Success", "User registration successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")
        finally:
            cursor.close()

    def update_password(self, new_password, user_id):
        try:
            query = """
                update users 
                set password = %s
                where id = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (new_password, user_id))
            self.connection.commit()
            messagebox.showinfo("Success", "User password updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update user password: {e}")
        finally:
            cursor.close()

    def find_user(self, phone, password):
        try:
            result = None
            query = """
                select * from users where phone = %s and password = %s;
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (phone, password))
            user = cursor.fetchone()
            if user:
                result = user
            return result
        except Exception as e:
            messagebox.showerror("Error", f"Failed to find user: {e}")
        finally:
            cursor.close()

    def find_rank(self):
        try:
            query = """
                select users.full_name as full_name, user_rank.score as score, user_rank.user_id
                from user_rank
                left join users
                    on user_rank.user_id = users.id
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch question: {e}")
        finally:
            cursor.close()
