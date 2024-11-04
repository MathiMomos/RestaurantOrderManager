import tkinter as tk
from tkinter import Canvas, PhotoImage, Entry, Button, messagebox
from pathlib import Path
from controllers.login_controller import LoginController
from views.admin_view import AdminView
from views.chef_view import ChefView
from views.caja_view import CajaView
from views.cliente_view import ClienteView
from views.panel_view import PanelView

class LoginView:
    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / "pictureLogin"

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def __init__(self, root):
        self.root = root
        self.root.title("Login - Restaurant Order Manager")
        self.root.geometry("1280x720")
        self.root.configure(bg="#FFFFFF")
        self.controller = LoginController()

        # Crear el lienzo (canvas)
        canvas = Canvas(
            self.root,
            bg="#FFFFFF",
            height=720,
            width=1280,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        canvas.place(x=0, y=0)

        # Cargar imágenes
        self.image_image_1 = PhotoImage(file=self.relative_to_assets("image_1.png"))
        canvas.create_image(639.0, 188.0, image=self.image_image_1)

        self.image_image_2 = PhotoImage(file=self.relative_to_assets("image_2.png"))
        canvas.create_image(639.0, 450.0, image=self.image_image_2)

        entry_image_1 = PhotoImage(file=self.relative_to_assets("entry_1.png"))
        canvas.create_image(639.5, 373.5, image=entry_image_1)

        # Entradas de usuario
        self.entry_username = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 14)
        )
        self.entry_username.place(
            x=371.0,
            y=351.0,
            width=537.0,
            height=45.0
        )

        canvas.create_text(
            359.0,
            312.0,
            anchor="nw",
            text="Nombre de usuario",
            fill="#34160E",
            font=("Inter", 20 * -1)
        )

        entry_image_2 = PhotoImage(file=self.relative_to_assets("entry_2.png"))
        canvas.create_image(639.5, 483.5, image=entry_image_2)

        self.entry_password = Entry(
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            highlightthickness=0,
            font=("Inter", 14),
            show="*"
        )

        self.password_visible = False  # Cambiamos la variable a un atributo de instancia

        self.entry_password.place(
            x=371.0,
            y=461.0,
            width=495.0,
            height=45.0
        )

        canvas.create_text(
            361.0,
            422.0,
            anchor="nw",
            text="Contraseña",
            fill="#34160E",
            font=("Inter", 20 * -1)
        )

        # Botón de Login
        button_image_1 = PhotoImage(file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.login,  # Conectamos el botón al método login
            relief="flat",
            background="#FFFFFF",
            activebackground="#FFFFFF"
        )
        button_1.place(
            x=359.0,
            y=532.0,
            width=562.0,
            height=49.0
        )

        # Botón para alternar la visibilidad de la contraseña
        button_image_2 = PhotoImage(file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            relief="flat",
            background="#FFFFFF",
            activebackground="#FFFFFF",
            command =self.toggle_password  # Conectamos el botón al método toggle_password
        )
        button_2.place(
            x=870.0,
            y=470.0,
            width=27.0,
            height=27.0
        )

        self.root.resizable(False, False)
        self.root.mainloop()

    def toggle_password(self):
        """Alterna la visibilidad de la contraseña."""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def login(self):
        """Maneja el proceso de login delegando la lógica al controlador."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        result = self.controller.validate_user(username, password)

        if result['status'] == 'success':
            user_id = result['user_id']
            role = result['role']
            messagebox.showinfo("Éxito", f"Bienvenido, {username}!")
            self.root.destroy()
            root = tk.Tk()
            root.geometry("1200x600")
            if role == 'admin':
                AdminView(root, user_id)
            elif role == 'chef':
                ChefView(root, user_id)
            elif role == 'caja':
                CajaView(root, user_id)
            elif role == 'mesa':
                ClienteView(root, user_id)
            elif role == 'panel':
                PanelView(root, user_id)
            else:
                messagebox.showerror("Error", "Rol no implementado aún.")
            root.mainloop()
        elif result['status'] == 'error':
            messagebox.showerror("Error", result['message'])