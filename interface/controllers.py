from tkinter import messagebox
from users import auth
import tkinter as tk

class Login:
    def __init__(self, view, app):
        self.view = view
        self.app = app
        self.view.login_btn.config(command=self.login)
        self.user = None

    def login(self):
        nick = self.view.nick_entr.get()
        password = self.view.pswrd_entr.get()

        user = auth(nick, password)

        if user:
            self.app.current_user_id = user
            self.view.destroy()

            if user[1] == "admin":
                messagebox.showinfo("Admin view!", "You have successfully logged in as an administrator!")
                self.app.show_admin_view()

            elif user:
                self.app.current_user_id = user
                messagebox.showinfo("Hello!", f"{user[1]}, you have successfully logged in!")
                self.app.show_main_view()
                self.view.destroy()
        else:
            messagebox.showerror("Error!", "Wrong nickname or password, try again!")

        self.user = user


class Main:
    def __init__(self, view, app):
        self.view = view
        self.app = app
        self.user = getattr(self.app, 'current_user_id', None)

        self.setup_view()

    def setup_view(self):
        if hasattr(self.view, 'welcome_label'):
            username = self.user[1]
            self.view.welcome_label.config(text=f"Welcome, {self.username}!")
        if hasattr(self.view, 'logout_button'):
            self.view.logout_button.config(command=self.logout)

    def logout(self):
        self.app.current_user_id = None
        self.app.show_login()
        self.view.destroy()

