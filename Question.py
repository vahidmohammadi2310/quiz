from tkinter import messagebox


class Question:
    def __init__(self, db_connection):
        self.connection = db_connection

    def create_question(self, title, option_a, option_b, option_c, option_d, correct_answer):
        try:
            query = """
                    insert into questions (title, opa, opb, opc, opd, correct_answer)
                    values(%s,%s,%s,%s,%s,%s);
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (title, option_a, option_b, option_c, option_d, correct_answer))
            self.connection.commit()
            messagebox.showinfo("Success", "Question created successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create question: {e}")
        finally:
            cursor.close()

    def edit_question(self,title, option_a, option_b, option_c, option_d, correct_answer, question_id):
        try:
            query = """
                update questions
                set title = %s, opa = %s, opb = %s, opc = %s , opd = %s, correct_answer = %s 
                where id = %s;
            """
            cursor = self.connection.cursor()
            cursor.execute(query,(title, option_a, option_b, option_c, option_d, correct_answer, question_id))
            self.connection.commit()
            messagebox.showinfo("Success", "Question updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update question: {e}")
        finally:
            cursor.close()

    def remove_question(self, question_id):
        try:
            query = """
                delete from questions
                where id = %s;
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (question_id,))
            self.connection.commit()
            messagebox.showinfo("Success", "Question removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove question: {e}")
        finally:
            cursor.close()

    def show_question(self, question_id):
        try:
            query = """
                select * from questions where id = %s
            """
            cursor = self.connection.cursor()
            cursor.execute(query, (question_id,))
            result = cursor.fetchone()
            if result:
                return result
            else:
                messagebox.showinfo("Info", "No question found with the given ID.")
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch question: {e}")
        finally:
            cursor.close()

    def get_all_questions(self):
        try:
            query = """
                select * from questions
            """
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch question: {e}")
        finally:
            cursor.close()

    def calculate_score(self, answers):
        questions = self.get_all_questions()
        score = 0
        for question in questions:
            for answer in answers:
                if question[0] == answer[0] and question[6] == answer[1]:
                    score += 1
        return score
