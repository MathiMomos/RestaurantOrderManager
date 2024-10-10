import tkinter as tk
from views.login_view import LoginView

if __name__ == "__main__":
    root = tk.Tk()
    login_view = LoginView(root)
    root.mainloop()
