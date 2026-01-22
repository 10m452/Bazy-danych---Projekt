import tkinter as tk


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

        self.logout_button = tk.Button(self, text="Wyloguj")
        self.logout_button.pack()



