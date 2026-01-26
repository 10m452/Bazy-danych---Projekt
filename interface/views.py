from datetime import date
import tkinter as tk
from tkinter import ttk
from sql_functions import get_movies, insert_review, insert_movies, movie_info, get_all_countries, get_all_directors, \
    get_all_genres, users_lists, movies_on_list, delete_from_list
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
        self.pswrd_entr= tk.Entry(self, width = 50, show="*")
        self.pswrd_entr.pack()

        self.login_btn = tk.Button(self, text="Login")
        self.login_btn.pack()

        self.register_btn = tk.Button(self, text="Register")
        self.register_btn.pack()

class MainFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        head = tk.Frame(self)
        head.pack(pady=10, fill="x")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand = True)
        self.tab_search = tk.Frame(self.notebook)
        self.tab_filter = tk.Frame(self.notebook)
        self.tab_top = tk.Frame(self.notebook)
        self.tab_reviews = tk.Frame(self.notebook)
        self.tab_personal = tk.Frame(self.notebook)
        self.tab_settings = tk.Frame(self.notebook)

        self.welcome_user = tk.Label(head, text="", font=("Arial", 12, "bold"))
        self.welcome_user.pack()
        self.welcome_label = tk.Label(head, text="Welcome to Our Movie Database! \n Here you can get inspiration from world of movies and share your cinematic experience with others!")
        self.welcome_label.pack()

        search = tk.LabelFrame(self.tab_search, text="Movie search and browser", padx=10, pady=10)
        search.pack(pady=10,fill="x", padx=20)
        search_fr = tk.Frame(search)
        search_fr.pack(fill="x")

        tk.Label(search_fr, text="Search a movie you want information about or write a review").pack()
        self.searchbar = tk.Entry(search_fr)
        search_var = tk.StringVar(self.searchbar, "")
        self.searchbar.config(textvariable=search_var)
        self.searchbar.pack()
        self.searchbut = tk.Button(search_fr, text="Search")
        self.searchbut.pack()
        self.browse_button = tk.Button(search_fr, text="Browse")
        self.browse_button.pack(pady=10)
        self.scroll_bar = tk.Scrollbar(search_fr)
        self.movie_list = tk.Listbox(search_fr, yscrollcommand=self.scroll_bar.set)
        self.sel_text = tk.Label(search_fr, text="Select movie:")
        self.select = ttk.Combobox(search_fr, state="readonly")
        self.choose = tk.Button(search_fr, text="Choose")

        fil = tk.LabelFrame(self.tab_filter, text="Movie search by filter", padx=10, pady=10)
        fil.pack(pady=10, fill="x", padx=20)
        fil_fr = tk.Frame(fil)
        fil_fr.pack(fill="x")
        self.filter = tk.Label(fil_fr, text="Filter by:")
        self.filter.pack()
        self.filter_val = tk.StringVar()
        self.scroll_bar_fil = tk.Scrollbar(fil_fr)
        self.movie_list_fil = tk.Listbox(fil_fr, yscrollcommand=self.scroll_bar_fil.set)
        radio_choice = tk.Frame(fil_fr)
        radio_choice.pack(pady=5)
        tk.Radiobutton(radio_choice, text="Genre", variable=self.filter_val, value="Genre").pack(side="left")
        tk.Radiobutton(radio_choice, text="Country", variable=self.filter_val, value="Country").pack(side="left")
        tk.Radiobutton(radio_choice, text="Director", variable=self.filter_val, value="Director").pack(side="left")
        tk.Radiobutton(radio_choice, text="Actor", variable=self.filter_val, value="Actor").pack(side="left")

        self.val_combo = ttk.Combobox(fil_fr, state="normal")
        self.val_combo.pack(pady=5)

        self.apply_filter = tk.Button(fil_fr, text="Apply filter")
        self.apply_filter.pack()

        top = tk.LabelFrame(self.tab_top, text="Best of the best", padx=10, pady=10)
        top.pack(pady=10, fill="x", padx=20)
        self.top_container = tk.Frame(top)
        self.top_container.pack(fill="x")
        self.top_button = tk.Button(self.top_container, text="Our TOP 10 movies by average rate")
        self.top_button.pack(pady=10)
        self.top_text = tk.Label(self.top_container,text="TOP 10 movies based on average rating", font=("Arial", 12, "bold"), wraplength=400, justify="left")

        rat = tk.LabelFrame(self.tab_reviews, text="My reviews", padx=10, pady=10)
        rat.pack(pady=10, fill="x", padx=20)
        rat_fr = tk.Frame(rat)
        rat_fr.pack(fill="x")
        self.show_reviews = tk.Button(rat_fr, text="Show my reviews")
        self.show_reviews.pack()
        self.revs = tk.Listbox(rat_fr, height = 10, width = 140)
        self.revs_scroll = tk.Scrollbar(rat_fr, command=self.revs.yview)
        self.revs.config(yscrollcommand=self.revs_scroll.set)
        self.scroll_bar_reviews = tk.Scrollbar(rat_fr)
        self.movie_list_reviews = tk.Listbox(rat_fr, yscrollcommand=self.scroll_bar_reviews.set)
        self.del_rate = tk.Button(rat_fr, text="Delete choosen rating")
        self.del_rate.pack()

        per = tk.LabelFrame(self.tab_personal, text="My watchlists & watched", padx=10, pady=10)
        per.pack(pady=10, fill="x", padx=20)
        per_fr = tk.Frame(per)
        per_fr.pack(fill="x")
        self.watchlists_button = tk.Button(per_fr, text="Manage your watchlists")
        self.watchlists_button.pack()
        self.watched_button = tk.Button(per_fr, text="Show watched movies")
        self.watched_button.pack()
        self.scroll_bar_watched = tk.Scrollbar(per_fr)
        self.movie_list_watched = tk.Listbox(per_fr, yscrollcommand=self.scroll_bar_watched.set)
        self.delwatched_button = tk.Button(per_fr, text="Delete choosen movie from watched")
        self.delwatched_button.pack()

        settings = tk.LabelFrame(self.tab_settings, text="Settings", padx=10, pady=10)
        settings.pack(pady=10, fill="x", padx=20)
        settings_fr = tk.Frame(settings)
        settings_fr.pack(fill="x")
        self.logout_button = tk.Button(settings_fr, text="Logout")
        self.logout_button.pack(side=tk.BOTTOM, pady=10)

        self.ch = tk.Label(settings_fr, text="New password: ")
        self.change_password = tk.Button(settings_fr, text="Change password")
        self.change_password.pack(side=tk.BOTTOM, pady=10)
        self.new = tk.Entry(settings_fr)
        self.confirm = tk.Button(settings_fr, text="Confirm")

        self.notebook.add(self.tab_search, text='Search and browse')
        self.notebook.add(self.tab_filter, text='Filter')
        self.notebook.add(self.tab_top, text='TOP10')
        self.notebook.add(self.tab_reviews, text="Reviews")
        self.notebook.add(self.tab_personal, text='Watchlists & watched')
        self.notebook.add(self.tab_settings, text='Settings')



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

        self.movie_average = tk.Label(self, text="", font=("Arial", 12, "bold"), wraplength=400, justify="left")
        self.movie_average.pack(pady=10)

        self.movie_country = tk.Label(self, text="")
        self.movie_country.pack()

        self.movie_genre = tk.Label(self, text="")
        self.movie_genre.pack()

        self.movie_dirs = tk.Label(self, text="")
        self.movie_dirs.pack()

        self.movie_cast = tk.Label(self, text="")
        self.movie_cast.pack()

        self.review_button = tk.Button(self, text="Write a review/rate a movie")
        self.review_button.pack()

        tk.Label(self, text="\n Add to watchlist \n Type a name of new list or choose an existing one:").pack()
        self.watchlist_lists = ttk.Combobox(self, state="normal")
        self.watchlist_lists.pack()

        self.add_to_list = tk.Button(self, text="Add to list")
        self.add_to_list.pack()

        self.mark_as_watched = tk.Button(self, text="Mark as watched")
        self.mark_as_watched.pack()

        self.reviews_button = tk.Button(self, text="Show movie's reviews")
        self.reviews_button.pack()

        self.reviews = tk.Text(self, height = 10, width = 120, wrap="word")
        self.reviews_scroll = tk.Scrollbar(self, command=self.reviews.yview)
        self.reviews.config(yscrollcommand=self.reviews_scroll.set)

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

        tk.Label(self, text="Release date:").pack()
        self.date_entry = tk.Entry(self, width=50)
        self.date_entry.pack()

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
        year = self.date_entry.get()
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

class WatchlistFrame(tk.Toplevel):
    def __init__(self, master, user):
        super().__init__(master)
        self.title("Watchlists panel")
        self.user = user

        tk.Label(self, text=f"You're in the watchlists panel. Here you can manage your lists.").pack()

        tk.Label(self, text="Select watchlist:").pack()
        self.select_watchlist = ttk.Combobox(self, state="readonly")
        self.select_watchlist['values'] = users_lists(self.user[0])
        self.select_watchlist.pack()

        self.choose_list = tk.Button(self, text="See movies on choosen list", command=self.mov_on_watchlist)
        self.choose_list.pack()
        self.ml = tk.Listbox(self)

        self.sel_to_delete = ttk.Combobox(self, state="readonly")
        self.prepare_delt = tk.Button(self, text="Delete from list", command=self.prepare_delt)
        self.delete = tk.Button(self, text="Delete", command=self.delete_from_watchlist)

        self.back = tk.Button(self, text="Back to main view", command=self.destroy)
        self.back.pack(side=tk.BOTTOM)

    def mov_on_watchlist(self):
        l_name = self.select_watchlist.get()
        self.ml.delete(0,tk.END)
        if not l_name:
            return
        for m in movies_on_list(l_name):
            self.ml.insert(tk.END, f'{m[0]} {m[1]} ({m[2]})')
        self.ml.pack()
        self.prepare_delt.pack()

    def prepare_delt(self):
        l_name = self.select_watchlist.get()
        if not l_name:
            return
        l = []
        for m in movies_on_list(l_name):
            l.append(f'{m[0]} {m[1]} ({m[2]})')
        self.sel_to_delete['values'] = l
        self.sel_to_delete.pack()
        self.delete.pack()
        movies = movies_on_list(l_name)
        self.map = {f'{m[0]} {m[1]} ({m[2]})': m[0] for m in movies}

    def delete_from_watchlist(self):
        l_name = self.select_watchlist.get()
        to_del = self.map.get(self.sel_to_delete.get())
        if to_del and l_name:
            try:
                delete_from_list(self.user[0], to_del,l_name)
                messagebox.showinfo("Success", "Movie removed from your list")
            except Exception as e:
                messagebox.showerror("Error", f"Something went wrong... {e}")


