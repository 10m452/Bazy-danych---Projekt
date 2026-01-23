from tkinter import messagebox, Scrollbar
from sql_functions import auth, get_movies, create_user, insert_movies, searchmovie, movie_info
import tkinter as tk
from views import ReviewFrame


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

    def top(self):
        ###TOP10###
        return

    def browse(self):
        self.view.scroll_bar.pack(side="right",fill = "both")

        movies = get_movies()
        self.mov_ids = {}

        for m in movies:
            s = f'{m[0]} {m[1]} ({m[2]})'
            self.view.movie_list.insert(tk.END, s)

            self.mov_ids[s] = m[0]

        self.view.movie_list.pack(side="left",fill = "both", expand=True)
        self.view.scroll_bar.config(command=self.view.movie_list.yview)
        self.view.movie_list.bind('<<ListboxSelect>>', self.on_select_movie)

    def on_select_movie(self, event):
        sel = self.view.movie_list.curselection()
        if sel:
            index = sel[0]
            selected = self.view.movie_list.get(index)

            movie_id = self.mov_ids.get(selected)
            if movie_id:
                self.app.show_movie_view(movie_id)

    def open_movie_view(self):
        choice = self.view.select.get()
        if not choice:
            messagebox.showwarning("Psst...", "You need to choose a movie!")
            return

        movie_id = self.movies_data.get(choice)
        print(f"DEBUG: Przekazuję movie_id: {movie_id}, typ: {type(movie_id)}")
        self.app.show_movie_view(movie_id)

    def search_movie(self):
        s = self.view.searchbar.get()
        res = searchmovie(s)

        self.movies_data = {f'{row[1]} ({row[2]}': row[0] for row in res}

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
            year = self.view.year_entry.get()
            length = self.view.length_entry.get()
            description = self.view.text.get("1.0",tk.END)

            insert_movies(title,year,length,description)
            messagebox.showinfo("Success", f"You added {title} to the database!")

            self.view.title_entry.delete(0,tk.END)
            self.view.year_entry.delete(0,tk.END)
            self.view.length_entry.delete(0,tk.END)
            self.view.text.delete("1.0",tk.END)
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

    def setup_view(self):
        username = self.user[1]
        data = movie_info(self.movie_id)

        if data:
            title = data[1]
            release_date = data[2]
            time = data[3]
            description = data[4]

        self.view.movie_label.config(text=f"Movie: {title}")
        self.view.movie_release.config(text=f"Release date: {release_date}")
        self.view.movie_length.config(text=f"Time (minutes): {time}")
        self.view.movie_description.config(text=f"Description: {description}")

        self.view.logout_button.config(command=self.logout)
        self.view.review_button.config(command=self.open_review_view)
        self.view.back.config(command=self.back_to_main)


    def open_review_view(self):
        ReviewFrame(self.app, self.user, self.movie_id)

    def back_to_main(self):
        self.view.destroy()
        self.app.show_main_view()



    def logout(self):
        self.app.current_user_id = None
        self.app.show_login()
        self.view.destroy()