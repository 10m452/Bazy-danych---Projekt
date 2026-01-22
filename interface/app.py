import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import psycopg2


## @file App.py
#  @brief Project of an application of simple budget manager.
#  @details Functions needed to display an app of a simple budget manager.

## Class App.
#
#  Creates main body of an app.
#
class App(tk.Tk):

    ## Initializer
    def __init__(self):
        super().__init__()
        self.title("MOVIES DATABASE")
        self.geometry("600x400")


        self.frames = {}

        for F in (MainFrame, LoginFrame):
            frame = F(self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, f):
        self.frames[f].tkraise()

## Class LoginFrame.
#
#  Creates an interface to login into an account.
#
class LoginFrame(tk.Frame):
    ## Initializer
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Hi! Welcome to Our Movie Data Base.").pack()
        login = tk.Label(self, text="Please enter your login (don't use any special symbols \n capital letters do not matter!): ")
        login.pack()
        self.login_entr = tk.Entry(self, width=50)
        self.login_entr.pack()


        pswrd = tk.Label(self, text = "Please enter your password: ")
        pswrd.pack()
        self.pswrd_entr= tk.Entry(self, width = 50)
        self.pswrd_entr.pack()



        tk.Button(self, text="Login", command=self.user_login).pack()
        tk.Button(self, text="Register", command=self.user_register).pack()

    ## Function that enables logging into an account.
    def user_login(self):
        login = self.login_entr.get().lower()
        password = self.pswrd_entr.get()
        clean = login.strip(r"!#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ")

        if not login or not password:
            messagebox.showwarning("Error!", "Please provide login and password.")
            return
        elif not self.master.um.auth(login, password):
            messagebox.showerror("Error!", "Wrong login or password.")
            return
        elif clean != login:
            messagebox.showerror("No special characters or whitespaces are allowed in your login. Please set new login.")

        else:
            self.master.bm_of_a_user = BudgetManager(login)
            messagebox.showinfo("Welcome!", "You've successfully logged into your account!")
            self.login_entr.delete(0, tk.END)
            self.pswrd_entr.delete(0, tk.END)

            self.master.show_frame("MainFrame")

    ## Function that enables registration process.
    def user_register(self):
        login = self.login_entr.get().lower()
        password = self.pswrd_entr.get()

        if login in self.master.um.load().keys():
            messagebox.showerror("Error", "Login occupied! Change login.")
        else:
            self.master.um.register(login, password)
            messagebox.showinfo("Welcome!", "You've successfully created an account!")
            self.master.bm_of_a_user = BudgetManager(login)

## Class MainFrame.
#
#  Creates an interface of main body of an app with all functions of Budget Manager.
#
class MainFrame(tk.Frame):
    ## Initializer.
    def __init__(self, master):
        super().__init__(master)

        self.welcome = tk.Label(self, text="")
        self.welcome.pack()

        menu = tk.Frame(self)
        menu.pack(side="left", fill="y")

        self.option = tk.Frame(self)
        self.option.pack(side="right", fill="both")

        click_button1 = tk.Button(self, text="Add transaction", width = 27, command = self.add_transaction)
        click_button2 = tk.Button(self, text="Show transactions in category", width = 27, command=self.show_transactions_for_category)
        click_button3 = tk.Button(self, text="Show balance", width = 27, command=self.show_balance)
        click_button4 = tk.Button(self, text="Show balance for specific date", width = 27, command = self.day_balance)
        click_button5 = tk.Button(self, text="Give money to another user", width = 27, command=self.transaction_to_other_user)
        click_button6 = tk.Button(self, text="Draw a pie chart of your expenses", width=27, command=self.plot_expenses)
        click_button7 = tk.Button(self, text="Set limit for a category", width = 27, command=self.set_limit_for_category)
        click_button8 = tk.Button(self, text="Save and end session", width = 27, command=self.save_and_logout)

        click_button1.pack()
        click_button2.pack()
        click_button3.pack()
        click_button4.pack()
        click_button5.pack()
        click_button6.pack()
        click_button7.pack()
        click_button8.pack()

    ## Clears widget in a window.
    def clear(self):
        for element in self.option.winfo_children():
            element.destroy()

    ## Sets up user's Budget Manager.
    def user_setup(self):
        user = self.master.bm_of_a_user.user
        self.welcome.config(text=f'Welcome, {user}! Let`s make your budget organised')

    ## Graphically represents adding transactions and accepts inputs from a user.
    def add_transaction(self):
        self.clear()
        tk.Label(self.option, text="Adding transaction").pack()

        tk.Label(self.option, text = "Type (income or expense): ").pack()
        type_entry = tk.Entry(self.option)
        type_entry.pack()

        tk.Label(self.option, text = "Amount: ").pack()
        amount_entry = tk.Entry(self.option)
        amount_entry.pack()

        tk.Label(self.option, text = "Category: ").pack()
        category_entry = tk.Entry(self.option)
        category_entry.pack()

        tk.Label(self.option, text = "Date (YYYY-MM-DD): ").pack()
        date_entry = tk.Entry(self.option)
        date_entry.pack()

        ## Accepts actions based on decisions and inputs of a user.
        def accept():
            type = type_entry.get().lower()
            try:
                amount = float(amount_entry.get())
                category = category_entry.get()
                date = date_entry.get()
                if type not in ["income", "expense"]:
                    raise ValueError("Wrong type! Must be an income or expense.")

                if self.master.bm_of_a_user.check_limit(category, amount):
                    decision = messagebox.askyesno("You`ve exceeded the limit!", f"Do you want to proceed adding an expense?")
                    if not decision:
                        messagebox.showinfo("Cancelled", "You've decided not to add this transaction. Be careful with your spendings!")
                        return
                type_entry.delete(0, tk.END)
                amount_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)

                self.master.bm_of_a_user.add_transaction(type, date, amount, category)
                messagebox.showinfo("Success", "You've successfully added your transaction.")
                self.option_clear()

            except ValueError:
                messagebox.showerror("Error!", "Wrong input.")

        tk.Button(self.option, text="Add", command=accept).pack()

    ## Graphically displays setting limit for category function.
    def set_limit_for_category(self):

        self.clear()
        tk.Label(self.option, text="Set limit for category").pack()

        tk.Label(self.option, text="Category: ").pack()
        category_entry = tk.Entry(self.option)
        category_entry.pack()

        tk.Label(self.option, text="Limit: ").pack()
        limit_entry = tk.Entry(self.option)
        limit_entry.pack()

        ## Accepts actions based on decisions and inputs of a user.
        def accept():
            try:
                limit = float(limit_entry.get())
                category = category_entry.get()
                if category not in self.master.bm_of_a_user.categories:
                    messagebox.showerror("Error", "Such category does not exist!")
                    return

                self.master.bm_of_a_user.categories[category].set_limit(limit)
                messagebox.showinfo("Limit set", f"You've successfully set limit for category {category} to {limit}.")
                limit_entry.delete(0, tk.END)
                category_entry.delete(0, tk.END)
                self.option_clear()
            except ValueError:
                messagebox.showerror("Error!", "Wrong input.")

        tk.Button(self.option, text="Done", command=accept).pack()

    ## Graphically represents showing transactions for a specific category.
    def show_transactions_for_category(self):
        self.clear()
        tk.Label(self.option, text="Show transactions in category").pack()

        tk.Label(self.option, text = "Category: ").pack()

        inside = tk.StringVar(self.option)
        options = list(self.master.bm_of_a_user.categories.keys())
        if not options:
            messagebox.showerror("Error", "No categories!")
            tk.Label(self.option, text="You don't have categories to show.").pack()
            return
        cat_options = tk.OptionMenu(self.option, inside, *options)
        cat_options.pack()

        ## Accepts actions based on decisions and inputs of a user.
        def action_stfc():
            category = inside.get()
            if category:
                try:
                    transactions = self.master.bm_of_a_user.show_transactions_for_category(category)
                except ValueError:
                    messagebox.showerror(title="Error!", message="Given category doesn't exist")
                    return
                self.option_clear()
                tk.Label(self.option, text=f"{transactions}").pack()
            else:
                messagebox.showwarning("No input", "Enter category")

        tk.Button(self.option, text="Show", command=action_stfc).pack()

    ## Graphically represents transaction to other user function.
    def transaction_to_other_user(self):

        self.clear()
        tk.Label(self.option, text="Transaction to other user").pack()

        tk.Label(self.option, text="Login of other user: ").pack()
        other_user_entry = tk.Entry(self.option)
        other_user_entry.pack()

        tk.Label(self.option, text="Amount: ").pack()
        amount_entry = tk.Entry(self.option)
        amount_entry.pack()

        tk.Label(self.option, text="Date (YYYY-MM-DD): ").pack()
        date_entry = tk.Entry(self.option)
        date_entry.pack()

        ## Accepts actions based on decisions and inputs of a user.
        def action_ttou():
            user = other_user_entry.get().lower()
            try:
                amount = float(amount_entry.get())
            except ValueError:
                messagebox.showerror("Error!", "Amount must be a number.")
            date = date_entry.get()
            if user and amount and date:
                try:
                    tk.Label(self.option, text=f'{self.master.bm_of_a_user.transaction_to_other_user(user, date, amount)}').pack()
                except ValueError:
                    messagebox.showerror("Error!", "User with this login doesn't exist")
                amount_entry.delete(0, tk.END)
                other_user_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                self.option_clear()
            else:
                messagebox.showwarning("Invalid input", "Enter data")

        tk.Button(self.option, text="Send", command=action_ttou).pack()

    ## Displays balance based on personal budget manager data.
    def show_balance(self):
        self.clear()
        tk.Label(self.option, text= f'{self.master.bm_of_a_user.balance()}').pack()

    ## Displays balance based on personal budget manager data.
    def day_balance(self):

        self.clear()
        tk.Label(self.option, text="Balance for a specific day").pack()

        tk.Label(self.option, text="Date (YYYY-MM-DD): ").pack()
        date_entry = tk.Entry(self.option)
        date_entry.pack()

        ## Accepts actions based on decisions and inputs of a user.
        def action_db():
            date = date_entry.get()
            if date:
                tk.Label(self.option, text = f' {self.master.bm_of_a_user.day_balance(date)}').pack()
                date_entry.delete(0, tk.END)
                self.option_clear()
            else:
                messagebox.showwarning("Invalid input", "Enter data")

        tk.Button(self.option, text="Show", command=action_db).pack()

    ## Displays graphically a plot of user's expenses.
    def plot_expenses(self):

        self.clear()
        fig = self.master.bm_of_a_user.plot_expenses()
        plot = FigureCanvasTkAgg(fig, self.option)
        plot.get_tk_widget().pack()
        plot.draw()
        plt.close(fig)

    ## Saves all data into a unique file and holds a process of logging out of an account.
    def save_and_logout(self):
        self.master.bm_of_a_user.save()
        messagebox.showinfo("Thank you, bye!", "You've successfully logged out of your account!")
        self.master.bm_of_a_user = None
        self.master.show_frame("LoginFrame")


if __name__ == "__main__":
    app = App()
    app.mainloop()