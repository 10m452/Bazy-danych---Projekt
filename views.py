from datetime import date
import tkinter as tk
from tkinter import ttk
from sql_functions import get_movies, insert_review, insert_movies
from tkinter import messagebox


class LoginFrame(tk.Frame):
    ## Initializer
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Hi! Welcome to Our Movie Data Base.").pack()

        login = tk.Label(self, text="Please enter your login (don't use any special symbols \n capital letters do not matter!): ")
        login.pack()

        self.nick_entr = tk.Entry(self, width=50)
        self.nick_entr.pack()

        pswrd = tk.Label(self, text = "Please enter your password: ")
        pswrd.pack()
        self.pswrd_entr= tk.Entry(self, width = 50)
        self.pswrd_entr.pack()

        self.login_btn = tk.Button(self, text="Login")
        self.login_btn.pack()

        self.register_btn = tk.Button(self, text="Register")
        self.register_btn.pack()

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.welcome_label = tk.Label(self, text="Witaj w naszej filmowej bazie danych! \n W tym świecie możesz zapoznać się z nowinkami w świecie filmowym, podzielić się opinią na ich temat \n i poznać innych kinomaniaków!")
        self.welcome_label.pack()

        self.welcome_user = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.welcome_user.pack()

        self.review_button = tk.Button(self, text="Write a review/rate a movie")
        self.review_button.pack()

        self.logout_button = tk.Button(self, text="Wyloguj")
        self.logout_button.pack()

class ReviewFrame(tk.Toplevel):
    def __init__(self, master, user):
        super().__init__(master)
        self.title("Review panel")
        self.user = user

        movies = get_movies()
        self.mov_list = {f'{m[1]} ({m[2]})': m[0] for m in movies}

        tk.Label(self, text="Share your thoughts about watched movies!").pack()

        tk.Label(self, text="Select movie:").pack()
        self.mov = ttk.Combobox(self, state="readonly")
        self.mov['values'] = list(self.mov_list.keys())
        self.mov.pack(pady=5)

        tk.Label(self, text="Rate movie in a scale from 1 to 10:").pack()
        self.v1 = tk.DoubleVar()
        self.sc = tk.Scale(self, variable=self.v1,from_=0, to=10, orient = tk.HORIZONTAL)
        self.sc.pack()

        tk.Label(self, text="Write a review (optional):").pack()
        self.text = tk.Text(self, height=5, width=40)
        self.text.pack()

        self.rate_button = tk.Button(self, text="Add review", command=self.add_review)
        self.rate_button.pack()

        self.back = tk.Button(self, text="Back to main view", command=self.destroy)
        self.back.pack()

    def add_review(self):
        selected_movie = self.mov.get()

        if not selected_movie:
            messagebox.showwarning("Warning!","Choose a movie!")
            return

        rate = self.sc.get()
        review = self.text.get("1.0",tk.END).strip()
        m_id = self.mov_list[selected_movie]
        print(f'Saving ID: {m_id}, Rating: {rate}, Review: {review}')
        today = date.today()

        try:
            insert_review(self.user[0], m_id, rate, today, review)
            messagebox.showinfo("Great!","New review has been added!")
            self.destroy()
        except Exception as e:
            print(e)
            messagebox.showerror("Oh...",f"Something went wrong: {e}")

class AdminFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.welcome_user = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.welcome_user.pack()

        tk.Label(self, text="Movie title:").pack()
        self.title_entry = tk.Entry(self, width=50)
        self.title_entry.pack()

        tk.Label(self, text="Year of production:").pack()
        self.year_entry = tk.Entry(self, width=50)
        self.year_entry.pack()

        tk.Label(self, text="Length (in minutes):").pack()
        self.length_entry = tk.Entry(self, width=50)
        self.length_entry.pack()

        tk.Label(self, text="Description:").pack()
        self.text = tk.Text(self, height=5, width=40)
        self.text.pack()

        self.upload = tk.Button(self, text="Add to library")
        self.upload.pack()

        self.logout_button = tk.Button(self, text="Logout")
        self.logout_button.pack()

    def add_movie(self):
        title = self.title_entry.get()
        year = int(self.year_entry.get())
        length = int(self.length_entry.get())
        description = self.text.get("1.0", tk.END).strip()
        insert_movies(title,year,length,description)