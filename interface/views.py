from datetime import date
import tkinter as tk
from tkinter import ttk
from sql_functions import get_movies, insert_review, insert_movies, movie_info
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

        self.welcome_label = tk.Label(self, text="Welcome to Our Movie Database! \n Here you can get inspiration from world of movies and share your cinematic experience with others!")
        self.welcome_label.pack()

        self.welcome_user = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.welcome_user.pack()

        tk.Label(self, text="Search a movie you want information about or write a review").pack()
        self.searchbar = tk.Entry(self)
        search_var = tk.StringVar(self.searchbar, "")
        self.searchbar.config(textvariable=search_var)
        self.searchbar.pack()
        self.searchbut = tk.Button(self, text="Search")
        self.searchbut.pack()

        self.top_button = tk.Button(self, text="Our TOP")
        self.top_button.pack(pady=10)

        self.browse_button = tk.Button(self, text="Browse")
        self.browse_button.pack(pady=10)
        self.scroll_bar = tk.Scrollbar(self)
        self.movie_list = tk.Listbox(self, yscrollcommand=self.scroll_bar.set)


        self.sel_text = tk.Label(self, text="Select movie:")
        self.select = ttk.Combobox(self, state="readonly")

        self.choose = tk.Button(self, text="Choose")

        self.logout_button = tk.Button(self, text="Logout")
        self.logout_button.pack(side=tk.BOTTOM, pady=10)

class MovieView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.movie_label = tk.Label(self,text="", font=("Arial", 12, "bold"))
        self.movie_label.pack()

        self.movie_release = tk.Label(self,text="", font=("Arial", 12, "bold"))
        self.movie_release.pack(pady=10)

        self.movie_length = tk.Label(self,text="", font=("Arial", 12, "bold"))
        self.movie_length.pack(pady=10)

        self.movie_description = tk.Label(self,text="", font=("Arial", 12, "bold"), wraplength=400, justify="left")
        self.movie_description.pack(pady=10)

        self.cast = tk.Label(self, text="")
        self.cast.pack()

        self.directors = tk.Label(self, text="")
        self.directors.pack()

        self.countries = tk.Label(self, text="")
        self.countries.pack()

        self.genres = tk.Label(self, text="")
        self.genres.pack()

        self.review_button = tk.Button(self, text="Write a review/rate a movie")
        self.review_button.pack()

        self.add_to_list = tk.Button(self, text="Add to list")
        self.add_to_list.pack()

        self.back = tk.Button(self, text="Back to main view")
        self.back.pack()

        self.logout_button = tk.Button(self, text="Logout")
        self.logout_button.pack(side=tk.BOTTOM, pady=10)

class ReviewFrame(tk.Toplevel):
    def __init__(self, master, user, movie_id):
        super().__init__(master)
        self.title("Review panel")
        self.user = user
        self.movie_id=movie_id

        title = movie_info(movie_id)[1]

        tk.Label(self, text=f"You're rating {title}").pack()

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
        selected_movie = self.movie_id

        if not selected_movie:
            messagebox.showwarning("Warning!","Choose a movie!")
            return

        rate = self.sc.get()
        review = self.text.get("1.0",tk.END).strip()
        today = date.today()

        try:
            insert_review(self.user[0], self.movie_id, rate, review)
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
        self.description_entry = tk.Text(self, width=50, height=5)
        self.description_entry.pack()

        tk.Label(self, text="Cast (please seperate with comma!):").pack()
        self.cast_entry = tk.Text(self, width=50, height=5)
        self.cast_entry.pack()

        tk.Label(self, text="Directors (please seperate with comma!):").pack()
        self.director_entry = tk.Text(self, width=50, height=4)
        self.director_entry.pack()

        tk.Label(self, text="Country (please seperate with comma!):").pack()
        self.country_entry = tk.Text(self, width=50, height=4)
        self.country_entry.pack()

        tk.Label(self, text="Genre (please seperate with comma!):").pack()
        self.genre_entry = tk.Text(self, width=50, height=4)
        self.genre_entry.pack()

        self.upload = tk.Button(self, text="Add to library")
        self.upload.pack()

        self.logout_button = tk.Button(self, text="Logout")
        self.logout_button.pack()

    def add_movie(self):
        title = self.title_entry.get()
        year = int(self.year_entry.get())
        length = int(self.length_entry.get())
        description = self.description_entry.get("1.0", tk.END).strip()
        cast = self.cast_entry.get("1.0", tk.END).strip()
        directors = self.director_entry.get("1.0", tk.END).strip()
        country =  self.country_entry.get("1.0", tk.END).strip()
        genre =  self.genre_entry.get("1.0", tk.END).strip()

        cast_list = [x.strip() for x in cast.split(",") if x.strip()]
        dir_list = [x.strip() for x in directors.split(",") if x.strip()]
        countries = [x.strip() for x in country.split(",") if x.strip()]
        genres = [x.strip() for x in genre.split(",") if x.strip()]

        insert_movies(title,year,length,description, cast_list, dir_list, countries, genres)
