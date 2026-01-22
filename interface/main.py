
import tkinter as tk

#from app import MainFrame
from views import LoginFrame, MainFrame
from controllers import Login, Main

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.current_user_id = None
        self.show_login()

    def show_login(self):
        self.view = LoginFrame(self)
        self.view.pack(expand=True, fill="both")
        Login(self.view, self)

    def show_main_view(self):
        self.view = MainFrame(self)
        self.view.pack(expand=True, fill="both")
        Main(self.view, self)



if __name__ == "__main__":
    App().mainloop()