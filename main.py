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

        # Add a button to show users
        # users_button = tk.Button(self.root, text="Users", command=self.show_user_list, bg="#2196F3", fg="white",
        #                          font=("Helvetica", 12))
        # users_button.pack(pady=10)

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
        QuestionManagerUI(self.root, self.question_manager, self.user_manager, user)  # Pass the logged-in user here

    def show_user_list(self):
        UserListWindow(self.root, self.user_manager)

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

        # Call the method to create the login form
        self.create_login_form()  # This method is now defined before it's called

    def create_login_form(self):
        # Clear the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Add login form widgets
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

        # Add registration form widgets
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
            self.login_success_callback(user)  # Pass the logged-in user to the callback
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

        self.user_manager.create_new_user(full_name, phone, password, age)
        self.create_login_form()  # Switch back to the login form after registration


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

        self.user_manager.create_new_user(full_name,phone, password, age)
        self.back_to_login()

    def back_to_login(self):
        self.login_callback()


class QuestionManagerUI:
    def __init__(self, master, question_manager, user_manager, user):
        self.master = master
        self.question_manager = question_manager
        self.user_manager = user_manager
        self.user = user  # Store the logged-in user

        self.master.title("Question Manager")
        self.master.geometry("600x400")
        self.master.configure(bg="#f0f0f0")

        # Title Label
        title_label = tk.Label(master, text="Question Manager", font=("Arial", 20), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.frame = tk.Frame(master, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Treeview for displaying questions
        self.tree = ttk.Treeview(self.frame, columns=('ID', 'Title'), show='headings', selectmode='browse')
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

        # Add Users Button
        self.users_button = tk.Button(button_frame, text="Users", command=self.show_user_list, width=20)
        self.users_button.grid(row=0, column=4, padx=5, pady=5)

        # Add Ranks Button
        self.ranks_button = tk.Button(button_frame, text="Ranks", command=self.show_ranks, width=20)
        self.ranks_button.grid(row=0, column=5, padx=5, pady=5)

        # Add Logout Button
        self.logout_button = tk.Button(button_frame, text="Logout", command=self.logout_user, width=20)
        self.logout_button.grid(row=0, column=6, padx=5, pady=5)

        self.update_password_button = tk.Button(button_frame, text="Update Password", command=self.show_update_password_window, width=20)
        self.update_password_button.grid(row=0, column=7, padx=5, pady=5)

        # Add Answer Question Button (Only for participants)
        if self.user[5] == 2:  # Assuming role is stored in the 6th index of the user tuple
            self.answer_button = tk.Button(button_frame, text="Answer Question", command=self.answer_question, width=20)
            self.answer_button.grid(row=0, column=7, padx=5, pady=5)

        self.load_questions()


    def show_update_password_window(self):
        """Open a new window to update the user's password."""
        UpdatePasswordWindow(self.master, self.user_manager, self.user[0])  # Pass the user_id

    def create_question(self):
        """Open the CreateQuestionWindow to add a new question."""
        CreateQuestionWindow(self.master, self.question_manager, self.load_questions)

    def load_questions(self):
        """Load questions from the database and display them in the Treeview."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        questions = self.question_manager.get_all_questions()
        for question in questions:
            self.tree.insert('', 'end', values=(question[0], question[1]))

    def edit_question(self):
        """Open the UpdateQuestionWindow to edit the selected question."""
        selected_item = self.tree.selection()
        if selected_item:
            question_id = self.tree.item(selected_item)['values'][0]
            question = self.question_manager.show_question(question_id)
            if question:
                UpdateQuestionWindow(self.master, self.question_manager, self.load_questions, question)
        else:
            messagebox.showwarning("Warning", "Please select a question to edit.")

    def remove_question(self):
        """Remove the selected question from the database."""
        selected_item = self.tree.selection()
        if selected_item:
            question_id = self.tree.item(selected_item)['values'][0]
            self.question_manager.remove_question(question_id)
            self.load_questions()
        else:
            messagebox.showwarning("Warning", "Please select a question to remove.")

    def view_question(self):
        """Display details of the selected question."""
        selected_item = self.tree.selection()
        if selected_item:
            question_id = self.tree.item(selected_item)['values'][0]
            question = self.question_manager.show_question(question_id)
            if question:
                messagebox.showinfo("Question Details", f"Title: {question[1]}\nOption A: {question[2]}\nOption B: {question[3]}\nOption C: {question[4]}\nOption D: {question[5]}\nCorrect Answer: {question[6]}")
        else:
            messagebox.showwarning("Warning", "Please select a question to view.")

    def show_user_list(self):
        """Open the UserListWindow to display all users."""
        UserListWindow(self.master, self.user_manager)

    def show_ranks(self):
        """Open the RanksWindow to display user ranks."""
        RanksWindow(self.master, self.user_manager)

    def logout_user(self):
        """Log out the current user and return to the login window."""
        self.master.destroy()
        MainApplication(self.user_manager.connection)

    def answer_question(self):
        """Open the AnswerQuestionWindow for participants to answer questions."""
        questions = self.question_manager.get_all_questions()  # Fetch all questions
        if questions:
            AnswerQuestionWindow(self.master, self.question_manager, self.user, questions, self.user_manager)
        else:
            messagebox.showwarning("Warning", "No questions available to answer.")


class UpdatePasswordWindow:
    def __init__(self, master, user_manager, user_id):
        self.master = master
        self.user_manager = user_manager
        self.user_id = user_id

        # Create a Toplevel window for the modal
        self.top = tk.Toplevel(master)
        self.top.title("Update Password")
        self.top.geometry("300x150")
        self.top.grab_set()  # Make this window modal
        self.top.focus_set()  # Focus on this window

        # Create a frame for styling
        self.frame = tk.Frame(self.top, bg="#ffffff", padx=20, pady=20)
        self.frame.pack(expand=True)

        # Add widgets for updating password
        tk.Label(self.frame, text="New Password:", bg="#ffffff", font=("Helvetica", 12)).pack(pady=5)
        self.new_password_entry = tk.Entry(self.frame, show='*', width=20, font=("Helvetica", 12))
        self.new_password_entry.pack(pady=5)

        # Submit Button
        submit_button = tk.Button(self.frame, text="Update Password", command=self.update_password, bg="#4CAF50", fg="white", font=("Helvetica", 12))
        submit_button.pack(pady=10)

    def update_password(self):
        """Update the user's password."""
        new_password = self.new_password_entry.get()

        if not new_password:
            messagebox.showerror("Error", "Please enter a new password.")
            return

        self.user_manager.update_password(new_password, self.user_id)
        messagebox.showinfo("Success", "Password updated successfully!")
        self.top.destroy()

class AnswerQuestionWindow:
    def __init__(self, master, question_manager, user, questions, user_manager):
        self.master = master
        self.question_manager = question_manager
        self.user = user
        self.questions = questions
        self.user_manager = user_manager
        self.current_question_index = 0
        self.answers = []

        # Create a modal window with better styling
        self.top = tk.Toplevel(master)
        self.top.title("Answer Questions")
        self.top.geometry("600x450")
        self.top.configure(bg="#f5f5f5")
        self.top.grab_set()
        self.top.focus_set()

        # Create main container with padding
        self.main_frame = tk.Frame(self.top, bg="white", highlightbackground="#e0e0e0", highlightthickness=1)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # Question Title with better styling
        self.question_label = tk.Label(self.main_frame, text="", font=("Helvetica", 16, "bold"), bg="white",
                                       wraplength=500)
        self.question_label.pack(pady=15, fill="x")

        # Options frame with better spacing
        self.options_frame = tk.Frame(self.main_frame, bg="white")
        self.options_frame.pack(pady=15, fill="x")

        # Radio buttons with improved styling
        self.option_var = tk.StringVar(value="")
        self.option_a = tk.Radiobutton(self.options_frame, text="", variable=self.option_var, value="opa",
                                       font=("Helvetica", 12), bg="white", anchor="w", selectcolor="white")
        self.option_a.pack(anchor='w', fill="x", padx=10, pady=5)

        self.option_b = tk.Radiobutton(self.options_frame, text="", variable=self.option_var, value="opb",
                                       font=("Helvetica", 12), bg="white", anchor="w", selectcolor="white")
        self.option_b.pack(anchor='w', fill="x", padx=10, pady=5)

        self.option_c = tk.Radiobutton(self.options_frame, text="", variable=self.option_var, value="opc",
                                       font=("Helvetica", 12), bg="white", anchor="w", selectcolor="white")
        self.option_c.pack(anchor='w', fill="x", padx=10, pady=5)

        self.option_d = tk.Radiobutton(self.options_frame, text="", variable=self.option_var, value="opd",
                                       font=("Helvetica", 12), bg="white", anchor="w", selectcolor="white")
        self.option_d.pack(anchor='w', fill="x", padx=10, pady=5)

        # Navigation Buttons with improved styling
        self.button_frame = tk.Frame(self.main_frame, bg="white")
        self.button_frame.pack(pady=15, fill="x")

        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.previous_question,
                                         bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"),
                                         state=tk.DISABLED, padx=10, pady=5)
        self.previous_button.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_question,
                                     bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
                                     padx=10, pady=5)
        self.next_button.pack(side=tk.LEFT, fill="x", expand=True, padx=5)

        # Submit Button with improved styling
        self.submit_button = tk.Button(self.main_frame, text="Submit", command=self.submit_answers,
                                       bg="#9C27B0", fg="white", font=("Helvetica", 12, "bold"),
                                       state=tk.DISABLED, padx=10, pady=5)
        self.submit_button.pack(pady=15, fill="x")

        self.load_question()

    def load_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question[1])

            # Clear any previous selection
            self.option_var.set("")

            # Update options with better formatting
            self.option_a.config(text=f"A) {question[2]}")
            self.option_b.config(text=f"B) {question[3]}")
            self.option_c.config(text=f"C) {question[4]}")
            self.option_d.config(text=f"D) {question[5]}")

            # Update button states
            self.previous_button.config(state=tk.NORMAL if self.current_question_index > 0 else tk.DISABLED)
            self.next_button.config(
                state=tk.NORMAL if self.current_question_index < len(self.questions) - 1 else tk.DISABLED)
            self.submit_button.config(
                state=tk.NORMAL if self.current_question_index == len(self.questions) - 1 else tk.DISABLED)
        else:
            self.top.destroy()

    def next_question(self):
        self.save_answer()
        self.current_question_index += 1
        self.load_question()

    def previous_question(self):
        self.current_question_index -= 1
        self.load_question()

    def save_answer(self):
        selected_option = self.option_var.get()
        if selected_option:
            question_id = self.questions[self.current_question_index][0]
            self.answers.append((question_id, selected_option))

    def submit_answers(self):
        self.save_answer()
        score = self.question_manager.calculate_score(self.answers)
        self.user_manager.update_score(score, self.user[0])
        messagebox.showinfo("Success", "Your answers have been submitted!")
        self.top.destroy()


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

        # Create a Toplevel window for the modal
        self.top = tk.Toplevel(master)
        self.top.title("User List")
        self.top.geometry("700x400")  # Adjusted width for additional column
        self.top.grab_set()  # Make this window modal
        self.top.focus_set()  # Focus on this window

        title_label = tk.Label(self.top, text="Registered Users", font=("Helvetica", 20), bg="#f0f0f0")
        title_label.pack(pady=10)

        self.frame = tk.Frame(self.top, bg="#ffffff", bd=2, relief=tk.GROOVE)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Treeview for displaying users, including Role column
        self.tree = ttk.Treeview(self.frame, columns=('Full Name',  'Role', 'Phone', 'Age', 'Register Date'), show='headings')

        # Center-aligning all columns
        for col in self.tree['columns']:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, anchor='center')  # Set the column anchor to center

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.load_users()

        # Add a button to close the modal
        close_button = tk.Button(self.top, text="Close", command=self.top.destroy, bg="#FF5722", fg="white", font=("Helvetica", 12))
        close_button.pack(pady=10)

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self.user_manager.user_list()
        for user in users:
            # Assuming user is a tuple of (full_name, phone, age, register_date, role)
            self.tree.insert('', 'end', values=user)


class RanksWindow:
    def __init__(self, master, user_manager):
        self.master = master
        self.user_manager = user_manager

        # Create a Toplevel window for the modal
        self.top = tk.Toplevel(master)
        self.top.title("User Ranks")
        self.top.geometry("400x300")  # Adjust width and height as needed
        self.top.grab_set()  # Make this window modal
        self.top.focus_set()  # Focus on this window

        title_label = tk.Label(self.top, text="User Ranks", font=("Helvetica", 16))
        title_label.pack(pady=10)

        self.frame = tk.Frame(self.top)
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Treeview for displaying ranks
        self.tree = ttk.Treeview(self.frame, columns=('Rank', 'Full Name', 'Score'), show='headings')

        # Center-aligning columns
        for col in self.tree['columns']:
            self.tree.heading(col, text=col, anchor='center')
            self.tree.column(col, anchor='center')  # Center-align the column

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.load_ranks()

        # Add a button to close the modal
        close_button = tk.Button(self.top, text="Close", command=self.top.destroy, bg="#FF5722", fg="white", font=("Helvetica", 12))
        close_button.pack(pady=10)

    def load_ranks(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        ranks = self.user_manager.find_rank()
        if ranks:
            for index, rank in enumerate(ranks, start=1):  # Start from 1 for ranking
                # Assuming rank is a tuple of (full_name, score, user_id)
                self.tree.insert('', 'end', values=(index, rank[0], rank[1]))  # Insert rank number, full name, and score


if __name__ == "__main__":
    db = Database('localhost', 'root', '', 'quiz')
    app = MainApplication(db.connection)