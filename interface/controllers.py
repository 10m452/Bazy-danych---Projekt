from multiprocessing.spawn import prepare
from tkinter import messagebox, Scrollbar
from sql_functions import del_watched, get_all_actors, movies_by_actor, movies_by_genre, directors_movies, \
    movies_from_country, \
    country, auth, genre, directors, get_movies, actors, create_user, insert_movies, searchmovie, movie_info, top_10, \
    get_all_genres, get_all_countries, \
    get_all_directors, show_user_reviews, users_lists, add_to_list, change_password, show_watched, mark_as_watched, \
    show_movie_review, delete_review, get_average_rate
import tkinter as tk
from views import ReviewFrame, WatchlistFrame


class Login:
    def __init__(self, view, app):
        self.view = view
        self.app = app
        self.view.login_btn.config(command=self.login)
        self.view.register_btn.config(command=self.register)
        self.user = None

    def login(self):
        nick = self.view.nick_entr.get()
        password = self.view.pswrd_entr.get()

        user = auth(nick, password)

        if not user and user is not None:
            messagebox.showerror("Error!",
                                 "Wrong nickname or password, try again!")
            self.view.nick_entr.delete(0,tk.END)
            self.view.pswrd_entr.delete(0,tk.END)
        elif user is None:
            messagebox.showerror("Error!", "Such account doesn't exist, please register.")
            self.view.nick_entr.delete(0,tk.END)
            self.view.pswrd_entr.delete(0,tk.END)
        else:
            self.app.current_user = user
            self.view.destroy()
            if user[1].lower() == "admin":
                messagebox.showinfo("Admin view!", "You have successfully logged in as an administrator!")
                self.app.show_admin_view()
            else:
                self.app.current_user = user
                messagebox.showinfo("Hello!", f"{user[1]}, you have successfully logged in!")
                self.app.show_main_view()
        self.user = user

    def register(self):
        nick = self.view.nick_entr.get()
        password = self.view.pswrd_entr.get()

        if nick=='' or password=='':
            messagebox.showerror("Error!", "Your nick and password cannot be empty!")
            return
        user = auth(nick, password)
        if not user:
            create_user(nick, password)
            messagebox.showinfo("Info","Account created successfully! Please log in.")
        else:
            messagebox.showerror("Error", "This account already exists! Please log in.")

class Main:
    def __init__(self, view, app):
        self.view = view
        self.app = app
        self.user = getattr(self.app, 'current_user', None)
        self.movies_data = {}
        self.setup_view()

    def setup_view(self):
        username = self.user[1]
        self.view.welcome_user.config(text=f"Welcome, {username}!")
        self.view.logout_button.config(command=self.logout)
        self.view.searchbut.config(command=self.search_movie)
        self.view.choose.config(command=self.open_movie_view)
        self.view.browse_button.config(command=self.browse)
        self.view.top_button.config(command=self.top)
        self.view.watchlists_button.config(command=self.open_watchlist_view)
        self.view.change_password.config(command=self.change_opt)
        self.view.watched_button.config(command=self.show_watched_movies)
        self.view.delwatched_button.config(command=self.delete_watched)
        self.view.show_reviews.config(command=self.prepare_del)
        self.view.del_rate.config(command=self.del_review)


        self.view.val_combo.bind("<KeyRelease>", self.handle_autocomplete)
        self.full_values_list = []
        self.view.filter_val.trace_add("write", lambda *args: self.update_filter_opt())

        self.view.apply_filter.config(command=self.filter)
        self.update_filter_opt()

    def change_opt(self):
        self.view.ch.pack()
        self.view.new.pack()
        self.view.confirm.pack()
        self.view.confirm.config(command=self.change_pass)

    def change_pass(self):
        id = self.user[0]
        new = self.view.new.get().strip()

        if not new:
            messagebox.showwarning("Warning", "Password cannot be empty!")
        try:
            change_password(id, new)
            messagebox.showinfo("Success", "Password changed!")
            self.view.new.pack_forget()
            self.view.confirm.pack_forget()
        except Exception as e:
            messagebox.showerror("Error", f'Fail: {e}')


    def open_watchlist_view(self):
        WatchlistFrame(self.app, self.user)

    def update_filter_opt(self):
        c = self.view.filter_val.get()

        if c == "Genre":
            self.full_values_list = get_all_genres()
        elif c == "Country":
            self.full_values_list = get_all_countries()
        elif c == "Director":
            self.full_values_list = get_all_directors()
        else:
            self.full_values_list = get_all_actors()

        self.view.val_combo['values'] = self.full_values_list
        self.view.val_combo.set(f'Select {c.lower()}')

    def handle_autocomplete(self, event):
        t = self.view.val_combo.get().lower()

        if t == '':
            data = self.full_values_list
        else:
            data = [i for i in self.full_values_list if t in i.lower()]
        self.view.val_combo['values'] = data

    def filter(self):
        filter_type = self.view.filter_val.get()
        filter_val = self.view.val_combo.get()

        if "Select" in filter_val or not filter_val:
            return

        map = {
            "Genre" : movies_by_genre,
            "Country" : movies_from_country,
            "Director" : directors_movies,
            "Actor" : movies_by_actor
        }

        sql_function = map.get(filter_type)
        if sql_function:
            self.view.movie_list_fil.delete(0,tk.END)
            res = sql_function(filter_val)
            self.mov_ids = {}

            for m in res:
                s = f'{m[0]} {m[1]} ({m[2]})'
                self.view.movie_list_fil.insert(tk.END, s)
                self.mov_ids[s] = m[0]

        self.view.scroll_bar_fil.pack(side="right", fill="y")
        self.view.movie_list_fil.pack(side="left", fill="both", expand=True)
        self.view.movie_list_fil.bind('<<ListboxSelect>>', self.on_select_movie)

    def top(self):
        top = top_10()
        self.view.top_text.pack()
        self.view.top_container.pack()
        for w in self.view.top_container.winfo_children():
            w.destroy()

        for m in list(top):
            t = f'{m[0]} - Average rate: {m[3]}'
            tk.Label(self.view.top_container, text = t).pack()

    def browse(self):
        self.view.scroll_bar.pack(side="right",fill = "both")

        movies = get_movies()
        self.view.movie_list.delete(0,tk.END)
        self.mov_ids = {}

        for m in movies:
            s = f'{m[0]} {m[1]} ({m[2]})'
            self.view.movie_list.insert(tk.END, s)

            self.mov_ids[s] = m[0]

        self.view.movie_list.pack(side="left",fill = "both", expand=True)
        self.view.scroll_bar.config(command=self.view.movie_list.yview)
        self.view.movie_list.bind('<<ListboxSelect>>', self.on_select_movie)

    def on_select_movie(self, event):
        sel = self.view.movie_list_fil.curselection()
        if sel:
            index = sel[0]
            selected = self.view.movie_list_fil.get(index)
            movie_id = self.mov_ids.get(selected)
            print(movie_id)
            #print(f'DEBUG: do bazy: {movie_id}')
            if movie_id:
                self.app.show_movie_view(movie_id)

    def open_movie_view(self):
        choice = self.view.select.get()
        if not choice:
            messagebox.showwarning("Psst...", "You need to choose a movie!")
            return

        movie_id = self.movies_data.get(choice)
        #print(f"DEBUG: Przekazuję movie_id: {movie_id}, typ: {type(movie_id)}")
        self.app.show_movie_view(movie_id)

    def show_watched_movies(self):
        watched = show_watched(self.user[0])
        self.view.movie_list_watched.delete(0, tk.END)
        self.mov_ids = {}

        for m in watched:

            s = f'{m[0]} {m[1]} ({m[2]})'
            self.view.movie_list_watched.insert(tk.END, s)
            self.mov_ids[s] = m[0]

        self.view.scroll_bar_watched.pack(side="right", fill="y")
        self.view.movie_list_watched.pack(side="left", fill="both", expand=True)


    def prepare_del(self):
        reviews = show_user_reviews(self.user[0])
        self.view.revs.pack()
        self.view.revs.delete(0,tk.END)
        self.rev_mov_ids = []
        if not reviews:
            messagebox.showinfo("Info", "No reviews to delete")
            return
        self.view.del_rate.pack()

        for r in reviews:
            key = f'Title: {r[1]} | Rating: {r[2]} | Review: {r[3]}'
            self.view.revs.insert(tk.END, key)
            self.rev_mov_ids.append(r[0])

    def del_review(self):
        sel = self.view.revs.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Select a review form the list!")
            return
        print(sel)
        print(self.rev_mov_ids)
        index = sel[0]
        movie_id = self.rev_mov_ids[index]
        print(movie_id)
        print(index)
        try:
            delete_review(self.user[0],movie_id)
            messagebox.showinfo("Success", "Review removed from your list")
            self.prepare_del()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong... {e}")

    def delete_watched(self):
        choice = self.view.movie_list_watched.curselection()
        print(choice)
        if not choice:
            messagebox.showwarning("Psst...", "You need to choose a movie!")
            return

        id = choice[0]
        mov_txt = self.view.movie_list_watched.get(id)
        movie_id = self.mov_ids.get(mov_txt)
        try:
            del_watched(self.user[0], movie_id)
            messagebox.showinfo("Success!", "Movie deleted from watched")
            self.show_watched_movies()
        except Exception as e:
            messagebox.showerror("Problem...", f"Something went wrong: {e}")

    def search_movie(self):
        s = self.view.searchbar.get()
        res = searchmovie(s)

        self.movies_data = {f'{row[1]} ({row[2]})': row[0] for row in res}

        self.view.sel_text.pack()
        self.view.select['values'] = list(self.movies_data.keys())
        self.view.select.pack(pady=5)
        self.view.choose.pack()

    def logout(self):
        self.app.current_user_id = None
        self.app.show_login()
        self.view.destroy()

class Admin:
    def __init__(self, view, app):
        self.view = view
        self.app = app
        self.user = getattr(self.app, 'current_user', None)
        self.setup_view()

    def setup_view(self):
        self.view.welcome_user.config(text=f"Admin Panel!")
        self.view.logout_button.config(command=self.logout)
        self.view.upload.config(command=self.add_movie)


    def add_movie(self):
        try:
            title = self.view.title_entry.get()
            date = self.view.date_entry.get()
            length = self.view.length_entry.get()
            description = self.view.description_entry.get("1.0",tk.END)

            if not title:
                raise ValueError("Title cannot be empty!")

            cast = self.view.cast_entry.get("1.0", tk.END).strip()
            directors = self.view.director_entry.get("1.0", tk.END).strip()
            country = self.view.country_entry.get("1.0", tk.END).strip()
            genre = self.view.genre_entry.get("1.0", tk.END).strip()

            cast_list = [x.strip() for x in cast.split(",") if x.strip()]
            dir_list = [x.strip() for x in directors.split(",") if x.strip()]
            countries = [x.strip() for x in country.split(",") if x.strip()]
            genres = [x.strip() for x in genre.split(",") if x.strip()]

            insert_movies(title, date, length, description, cast_list, dir_list, countries, genres)
            messagebox.showinfo("Success", f"You added {title} to the database!")

            self.view.title_entry.delete(0,tk.END)
            self.view.date_entry.delete(0,tk.END)
            self.view.length_entry.delete(0,tk.END)
            self.view.description_entry.delete("1.0",tk.END)
            self.view.cast_entry.delete(0, tk.END)
            self.view.director_entry.delete(0, tk.END)
            self.view.country_entry.delete(0, tk.END)
            self.view.genre_entry.delete("1.0", tk.END)
        except ValueError:
            messagebox.showerror("Error", "Year and length (min) must be integers")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def logout(self):
        self.app.current_user_id = None
        self.app.show_login()
        self.view.destroy()

class Movie:
    def __init__(self, view, app, movie_id):
        self.view = view
        self.app = app
        self.movie_id = movie_id
        self.user = getattr(self.app, 'current_user', None)
        self.setup_view()
        self.update_watchlists()

    def setup_view(self):
        username = self.user[1]
        data = movie_info(self.movie_id)

        if data:
            title = data[1]
            release_date = data[2]
            time = data[3]
            description = data[4]
            if get_average_rate(self.movie_id) is not None:
                average = float(get_average_rate(self.movie_id)[0])
            else:
                average = 'No ratings to calculate average rate.'
            cast = actors(self.movie_id)
            dir = directors(self.movie_id)
            c = country(self.movie_id)
            gen = genre(self.movie_id)

        self.view.movie_label.config(text=f"Movie: {title}")
        self.view.movie_release.config(text=f"Release date: {release_date}")
        self.view.movie_length.config(text=f"Time (minutes): {time}")
        self.view.movie_description.config(text=f"Description: {description}")
        self.view.movie_average.config(text=f'Average rate: {average}')
        self.view.movie_genre.config(text=f"Genre: {gen}")
        self.view.movie_country.config(text=f"Country: {c}")
        self.view.movie_cast.config(text=f"Cast: {cast}")
        self.view.movie_dirs.config(text=f"Directors: {dir}")

        self.view.add_to_list.config(command=self.add_to_watchlist)
        self.view.mark_as_watched.config(command=self.mark_as_watched)
        self.view.logout_button.config(command=self.logout)
        self.view.review_button.config(command=self.open_review_view)
        self.view.reviews_button.config(command=self.show_reviews)
        self.view.back.config(command=self.back_to_main)

    def open_review_view(self):
        ReviewFrame(self.app, self.user, self.movie_id)

    def show_reviews(self):
        revs = show_movie_review(self.movie_id)
        for r in revs:
            s = f'   --- \n Nick: {r[1]} \n Rating: {r[2]} \n Review: {r[3]}) \n    --- \n'
            self.view.reviews.insert(tk.END, s)
        self.view.reviews.pack()


    def mark_as_watched(self):
        try:
            mark_as_watched(self.movie_id, self.user[0])
            messagebox.showinfo("Hurray!", "Another movie marked as watched!")
        except Exception as e:
            messagebox.showerror("Problem...", f"Something went wrong: {e}")

    def back_to_main(self):
        self.view.destroy()
        self.app.show_main_view()

    def add_to_watchlist(self):
        list_name = self.view.watchlist_lists.get().strip()
        if not list_name or "Name your first" in list_name:
            messagebox.showwarning("Warning", "Enter/select a list")
            return
        print(self.movie_id)
        print(list_name)
        print(self.user[0])
        try:
            add_to_list(self.movie_id, self.user[0], list_name)
            messagebox.showinfo("Great!", "Successfully added this movie to a watchlist!")
            self.update_watchlists()
        except Exception as e:
            messagebox.showerror("Error", f"Something went wrong... {e}")

    def update_watchlists(self):
        lists = users_lists(self.user[0])
        print(lists)
        self.view.watchlist_lists['values']=lists

        if len(lists) > 0:
            self.view.watchlist_lists.set("Choose list/add a new list")
        else:
            self.view.watchlist_lists.set("Name your first watchlist")

    def logout(self):
        self.app.current_user_id = None
        self.app.show_login()
        self.view.destroy()

