from DatabaseConnection import Database
import tkinter as tk
from tkinter import ttk, messagebox
from Question import Question
from User import User


class MainApplication:
    def __init__(self, db_connection):
        self.root = tk.Tk()
        self.db = db_connection
        self.user_manager = User(db_connection)
        self.question_manager = Question(db_connection)

        self.root.title("Quiz Application")
        self.root.geometry("400x300")
        self.show_login_window()
        self.root.mainloop()

    def show_login_window(self):
        self.clear_window()
        LoginWindow(self.root, self.user_manager, self.show_register_window, self.show_question_manager)

    def show_register_window(self):
        self.clear_window()
        RegisterWindow(self.root, self.user_manager, self.show_login_window)

    def show_question_manager(self, user):
        self.clear_window()
        QuestionManagerUI(self.root, self.question_manager)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


class LoginWindow:
    def __init__(self, master, user_manager, register_callback, login_success_callback):
        self.master = master
        self.user_manager = user_manager
        self.register_callback = register_callback
        self.login_success_callback = login_success_callback

        # Create a main frame
        self.frame = tk.Frame(master, bg="#ffffff", padx=20, pady=20)
        self.frame.pack(expand=True)

        self.create_login_form()

    def create_login_form(self):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Login", font=("Helvetica", 24, 'bold'), bg="#ffffff").pack(pady=10)

        tk.Label(self.frame, text="Phone:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.phone_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.phone_entry.pack(pady=5)

        tk.Label(self.frame, text="Password:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', width=30, font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        login_button = tk.Button(self.frame, text="Login", command=self.login, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        login_button.pack(pady=10)

        # Switch to registration
        switch_button = tk.Button(self.frame, text="Don't have an account? Register", command=self.create_register_form, bg="#2196F3", fg="white", font=("Helvetica", 12))
        switch_button.pack(pady=5)

    def create_register_form(self):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        tk.Label(self.frame, text="Register", font=("Helvetica", 24, 'bold'), bg="#ffffff").pack(pady=10)

        tk.Label(self.frame, text="Full Name:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.name_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        tk.Label(self.frame, text="Phone:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.phone_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.phone_entry.pack(pady=5)

        tk.Label(self.frame, text="Password:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', width=30, font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        tk.Label(self.frame, text="Age:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.age_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.age_entry.pack(pady=5)

        register_button = tk.Button(self.frame, text="Register", command=self.register, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        register_button.pack(pady=10)

        # Switch to login
        switch_button = tk.Button(self.frame, text="Already have an account? Login", command=self.create_login_form, bg="#FF5722", fg="white", font=("Helvetica", 12))
        switch_button.pack(pady=5)

    def login(self):
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        user = self.user_manager.find_user(phone, password)

        if user:
            messagebox.showinfo("Success", "Login successful!")
            self.login_success_callback(user)
        else:
            messagebox.showerror("Error", "Invalid phone or password.")

    def register(self):
        full_name = self.name_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        age = self.age_entry.get()

        if not full_name or not phone or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.user_manager.create_new_user(full_name, None, phone, password, age)
        messagebox.showinfo("Success", "Registration successful!")
        self.create_login_form()


class RegisterWindow:
    def __init__(self, master, user_manager, login_callback):
        self.master = master
        self.user_manager = user_manager
        self.login_callback = login_callback

        # Create a frame for styling
        self.frame = tk.Frame(master, bg="#ffffff", padx=20, pady=20)
        self.frame.pack(expand=True)

        tk.Label(self.frame, text="Register", font=("Helvetica", 24, 'bold'), bg="#ffffff").pack(pady=10)

        tk.Label(self.frame, text="Full Name:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.name_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.name_entry.pack(pady=5)

        tk.Label(self.frame, text="Phone:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.phone_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.phone_entry.pack(pady=5)

        tk.Label(self.frame, text="Password:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.password_entry = tk.Entry(self.frame, show='*', width=30, font=("Helvetica", 12))
        self.password_entry.pack(pady=5)

        tk.Label(self.frame, text="Age:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.age_entry = tk.Entry(self.frame, width=30, font=("Helvetica", 12))
        self.age_entry.pack(pady=5)

        # Styled buttons
        register_button = tk.Button(self.frame, text="Register", command=self.register, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        register_button.pack(pady=10)

        back_button = tk.Button(self.frame, text="Back to Login", command=self.back_to_login, bg="#FF5722", fg="white", font=("Helvetica", 12))
        back_button.pack(pady=5)

    def register(self):
        full_name = self.name_entry.get()
        phone = self.phone_entry.get()
        password = self.password_entry.get()
        age = self.age_entry.get()

        if not full_name or not phone or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.user_manager.create_new_user(full_name, None, phone, password, age)
        messagebox.showinfo("Success", "Registration successful!")
        self.back_to_login()

    def back_to_login(self):
        self.login_callback()


class QuestionManagerUI:
    def __init__(self, master, question_manager):
        self.master = master
        self.question_manager = question_manager

        self.master.title("Question Manager")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f0")

        # Title Label
        title_label = tk.Label(master, text="Question Manager", font=("Arial", 20), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.frame = tk.Frame(master, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Treeview for displaying questions
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Title'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Title', text='Question Title')
        self.tree.column('ID', width=50)
        self.tree.column('Title', width=450)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Button Frame
        button_frame = tk.Frame(master, bg="#f0f0f0")
        button_frame.pack(pady=10)

        # Buttons
        self.create_button = tk.Button(button_frame, text="Create New Question", command=self.create_question, width=20)
        self.create_button.grid(row=0, column=0, padx=5, pady=5)

        self.edit_button = tk.Button(button_frame, text="Edit Question", command=self.edit_question, width=20)
        self.edit_button.grid(row=0, column=1, padx=5, pady=5)

        self.remove_button = tk.Button(button_frame, text="Remove Question", command=self.remove_question, width=20)
        self.remove_button.grid(row=0, column=2, padx=5, pady=5)

        self.view_button = tk.Button(button_frame, text="View Question", command=self.view_question, width=20)
        self.view_button.grid(row=0, column=3, padx=5, pady=5)

        self.load_questions()

    def load_questions(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        questions = self.question_manager.get_all_questions()
        for question in questions:
            self.tree.insert('', 'end', values=(question[0], question[1]))

    def create_question(self):
        CreateQuestionWindow(self.master, self.question_manager, self.load_questions)

    def edit_question(self):
        selected_item = self.tree.selection()
        if selected_item:
            question_id = self.tree.item(selected_item)['values'][0]
            question = self.question_manager.show_question(question_id)
            if question:
                UpdateQuestionWindow(self.master, self.question_manager, self.load_questions, question)
        else:
            messagebox.showwarning("Warning", "Please select a question to edit.")

    def remove_question(self):
        selected_item = self.tree.selection()
        if selected_item:
            question_id = self.tree.item(selected_item)['values'][0]
            self.question_manager.remove_question(question_id)
            self.load_questions()
        else:
            messagebox.showwarning("Warning", "Please select a question to remove.")

    def view_question(self):
        selected_item = self.tree.selection()
        if selected_item:
            question_id = self.tree.item(selected_item)['values'][0]
            question = self.question_manager.show_question(question_id)
            if question:
                messagebox.showinfo("Question Details",
                                    f"Title: {question[1]}\nOptions:\nA: {question[2]}\nB: {question[3]}\nC: {question[4]}\nD: {question[5]}\nCorrect Answer: {question[6]}")
        else:
            messagebox.showwarning("Warning", "Please select a question to view.")


class CreateQuestionWindow:
    def __init__(self, master, question_manager, refresh_callback):
        self.top = tk.Toplevel(master)
        self.top.title("Create New Question")
        self.top.configure(bg="#f0f0f0")
        self.question_manager = question_manager
        self.refresh_callback = refresh_callback

        # Question Title
        tk.Label(self.top, text="Question Title:", bg="#f0f0f0").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.title_entry = tk.Entry(self.top, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Options
        tk.Label(self.top, text="Option A:", bg="#f0f0f0").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.option_a_entry = tk.Entry(self.top, width=50)
        self.option_a_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Option B:", bg="#f0f0f0").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.option_b_entry = tk.Entry(self.top, width=50)
        self.option_b_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Option C:", bg="#f0f0f0").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.option_c_entry = tk.Entry(self.top, width=50)
        self.option_c_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.top, text="Option D:", bg="#f0f0f0").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.option_d_entry = tk.Entry(self.top, width=50)
        self.option_d_entry.grid(row=4, column=1, padx=5, pady=5)

        # Correct Answer
        tk.Label(self.top, text="Correct Answer:", bg="#f0f0f0").grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.correct_answer_entry = tk.Entry(self.top, width=50)
        self.correct_answer_entry.grid(row=5, column=1, padx=5, pady=5)

        # Submit Button
        self.submit_button = tk.Button(self.top, text="Create Question", command=self.submit)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    def submit(self):
        title = self.title_entry.get()
        option_a = self.option_a_entry.get()
        option_b = self.option_b_entry.get()
        option_c = self.option_c_entry.get()
        option_d = self.option_d_entry.get()
        correct_answer = self.correct_answer_entry.get()

        if correct_answer not in ['opa', 'opb', 'opc', 'opd']:
            messagebox.showerror("Error", "Correct answer must be one of 'opa', 'opb', 'opc', or 'opd'.")
            return

        self.question_manager.create_question(title, option_a, option_b, option_c, option_d, correct_answer)
        self.refresh_callback()
        self.top.destroy()


class UpdateQuestionWindow:
    def __init__(self, master, question_manager, refresh_callback, question):
        self.top = tk.Toplevel(master)
        self.top.title("Update Question")
        self.top.configure(bg="#f0f0f0")
        self.question_manager = question_manager
        self.refresh_callback = refresh_callback
        self.question = question

        # Question Title
        tk.Label(self.top, text="Question Title:", bg="#f0f0f0").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.title_entry = tk.Entry(self.top, width=50)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)
        self.title_entry.insert(0, question[1])

        # Options
        tk.Label(self.top, text="Option A:", bg="#f0f0f0").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.option_a_entry = tk.Entry(self.top, width=50)
        self.option_a_entry.grid(row=1, column=1, padx=5, pady=5)
        self.option_a_entry.insert(0, question[2])

        tk.Label(self.top, text="Option B:", bg="#f0f0f0").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.option_b_entry = tk.Entry(self.top, width=50)
        self.option_b_entry.grid(row=2, column=1, padx=5, pady=5)
        self.option_b_entry.insert(0, question[3])

        tk.Label(self.top, text="Option C:", bg="#f0f0f0").grid(row=3, column=0, sticky='e', padx=5, pady=5)
        self.option_c_entry = tk.Entry(self.top, width=50)
        self.option_c_entry.grid(row=3, column=1, padx=5, pady=5)
        self.option_c_entry.insert(0, question[4])

        tk.Label(self.top, text="Option D:", bg="#f0f0f0").grid(row=4, column=0, sticky='e', padx=5, pady=5)
        self.option_d_entry = tk.Entry(self.top, width=50)
        self.option_d_entry.grid(row=4, column=1, padx=5, pady=5)
        self.option_d_entry.insert(0, question[5])

        # Correct Answer
        tk.Label(self.top, text="Correct Answer:", bg="#f0f0f0").grid(row=5, column=0, sticky='e', padx=5, pady=5)
        self.correct_answer_entry = tk.Entry(self.top, width=50)
        self.correct_answer_entry.grid(row=5, column=1, padx=5, pady=5)
        self.correct_answer_entry.insert(0, question[6])

        # Submit Button
        self.submit_button = tk.Button(self.top, text="Update Question", command=self.submit)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    def submit(self):
        title = self.title_entry.get()
        option_a = self.option_a_entry.get()
        option_b = self.option_b_entry.get()
        option_c = self.option_c_entry.get()
        option_d = self.option_d_entry.get()
        correct_answer = self.correct_answer_entry.get()

        if correct_answer not in ['opa', 'opb', 'opc', 'opd']:
            messagebox.showerror("Error", "Correct answer must be one of 'opa', 'opb', 'opc', or 'opd'.")
            return

        question_id = self.question[0]
        self.question_manager.edit_question(title, option_a, option_b, option_c, option_d, correct_answer, question_id)
        self.refresh_callback()
        self.top.destroy()


class UserListWindow:
    def __init__(self, master, user_manager):
        self.master = master
        self.user_manager = user_manager

        self.master.title("User List")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f0")

        title_label = tk.Label(master, text="Registered Users", font=("Helvetica", 20), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.frame = tk.Frame(master, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Treeview for displaying users
        self.tree = ttk.Treeview(self.frame, columns=('Full Name', 'Phone', 'Age', 'Register Date', 'Role'), show='headings')
        self.tree.heading('Full Name', text='Full Name')
        self.tree.heading('Phone', text='Phone')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Register Date', text='Register Date')
        self.tree.heading('Role', text='Role')
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.load_users()

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self.user_manager.user_list()
        for user in users:
            self.tree.insert('', 'end', values=user)


if __name__ == "__main__":
    db = Database('localhost', 'root', '', 'quiz')
    app = MainApplication(db.connection)