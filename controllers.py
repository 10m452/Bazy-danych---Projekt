from tkinter import messagebox
from sql_functions import auth, create_user, insert_movies
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
        self.setup_view()

    def setup_view(self):
        username = self.user[1]
        self.view.welcome_user.config(text=f"Welcome, {username}!")
        self.view.logout_button.config(command=self.logout)
        self.view.review_button.config(command=self.open_review_view)

    def open_review_view(self):
        ReviewFrame(self.app, self.user)

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