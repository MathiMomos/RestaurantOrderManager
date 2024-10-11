import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import LoginController

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1200x600")
        self.root.configure(bg="#F0F0F0")
        canvas = tk.Canvas(self.root, width=500, height=500, bg="#F0F0F0", highlightthickness=0)
        canvas.place(relx=0.5, rely=0.5, anchor="center")
        self.round_rectangle(canvas, 50, 50, 450, 450, radius=50, fill="#D3D3D3", outline="#2F2F2F", width=2)
        title = tk.Label(self.root, text="LOGIN", font=("Helvetica", 32, "bold"), bg="#D3D3D3", fg="#333")
        title.place(relx=0.5, rely=0.25, anchor="center")
        user_label = tk.Label(self.root, text="USUARIO", font=("Helvetica", 14), bg="#D3D3D3", fg="#333")
        user_label.place(relx=0.5, rely=0.38, anchor="center")
        self.username = tk.Entry(self.root, font=("Helvetica", 12))
        self.username.place(relx=0.5, rely=0.43, anchor="center", width=250, height=30)
        password_label = tk.Label(self.root, text="CONTRASEÑA", font=("Helvetica", 14), bg="#D3D3D3", fg="#333")
        password_label.place(relx=0.5, rely=0.53, anchor="center")
        self.password = tk.Entry(self.root, font=("Helvetica", 12), show="*")
        self.password.place(relx=0.5, rely=0.58, anchor="center", width=250, height=30)
        self.show_password_var = tk.IntVar()
        show_password_check = tk.Checkbutton(self.root, text="Ver Contraseña", variable=self.show_password_var,
                                             onvalue=1, offvalue=0, command=self.toggle_password, bg="#D3D3D3")
        show_password_check.place(relx=0.5, rely=0.65, anchor="center")
        login_button = tk.Button(self.root, text="Login", font=("Helvetica", 14), command=self.login)
        login_button.place(relx=0.5, rely=0.75, anchor="center", width=150, height=40)
        self.controller = LoginController()

    def round_rectangle(self, canvas, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1 + radius, y1,
                  x1 + radius, y1,
                  x2 - radius, y1,
                  x2 - radius, y1,
                  x2, y1,
                  x2, y1 + radius,
                  x2, y1 + radius,
                  x2, y2 - radius,
                  x2, y2 - radius,
                  x2, y2,
                  x2 - radius, y2,
                  x2 - radius, y2,
                  x1 + radius, y2,
                  x1 + radius, y2,
                  x1, y2,
                  x1, y2 - radius,
                  x1, y2 - radius,
                  x1, y1 + radius,
                  x1, y1 + radius,
                  x1, y1]
        return canvas.create_polygon(points, **kwargs, smooth=True)

    def toggle_password(self):
        if self.show_password_var.get():
            self.password.config(show="")
        else:
            self.password.config(show="*")

    def login(self):
        username = self.username.get()
        password = self.password.get()
        result = self.controller.login(username, password)
        print(result)
        if result and "error" not in result:
            messagebox.showinfo("Bienvenido", f"Bienvenido {result['username']}, Rol: {result['role']}")
            self.root.destroy()
            self.open_menu_by_role(result['role'], result['username'])
        else:
            messagebox.showerror("Error", result.get("error", "Error desconocido"))

    def open_menu_by_role(self, role, username):
        print(f"Rol: {role}, Nombre de usuario: {username}")
        if role == "admin":
            from views.admin_view import AdminView
            admin_root = tk.Tk()
            AdminView(admin_root)
            admin_root.mainloop()
        elif role == "cliente":
            from views.cliente_view import ClienteView
            cliente_root = tk.Tk()
            ClienteView(cliente_root, username)
            cliente_root.mainloop()
        elif role == "panel":
            from views.panel_view import PanelView
            panel_root = tk.Tk()
            PanelView(panel_root)
            panel_root.mainloop()
        elif role == "chef":
            from views.chef_view import ChefView
            chef_root = tk.Tk()
            ChefView(chef_root)
            chef_root.mainloop()
        elif role == "caja":
            from views.caja_view import CajaView
            caja_root = tk.Tk()
            CajaView(caja_root)
            caja_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login_view = LoginView(root)
    root.mainloop()
