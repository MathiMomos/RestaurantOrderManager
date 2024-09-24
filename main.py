from controllers.login_controller import autenticar_usuario
from data.database import crear_tablas
import tkinter as tk

def main():
    crear_tablas()

    window=tk.Tk()
    window.title("El Criollito Restaurant Manager")
    window.geometry("1200x625")

    label = tk.Label(window, text="Bienvenido al Criollito", font=("sans-serif", 20))
    label2 = tk.Label(window, text="Gestor de Restaurante", font=("Sans-serif", 15))
    label.pack(pady=10)
    label2.pack(pady=10)

    usuario_label = tk.Label(window, text="Usuario:", font=("sans-serif", 15))
    usuario_label.pack(pady=5)
    usuario_entry = tk.Entry(window)
    usuario_entry.pack(pady=5)

    pass_label = tk.Label(window, text="Contraseña:", font=("sans-serif", 15))
    pass_label.pack(pady=5)
    pass_entry = tk.Entry(window)
    pass_entry.pack(pady=5)

    mensaje_label = tk.Label(window, text="", font=("sans-serif", 15))
    mensaje_label.pack(pady=10)

    def login_usuario(usuario_entry, pass_entry, mensaje_label, window):
        nombre = usuario_entry.get()
        contrasena = pass_entry.get()

        usuario = autenticar_usuario(nombre, contrasena)

        if usuario:
            mensaje_label.config(text=f"Bienvenido, {usuario.nombre}. Eres un {usuario.tipo}.", font=("sans-serif", 15))

            if usuario.tipo == 'admin':
                mensaje_label.config(text="Accediendo al menú de administrador...", font=("sans-serif", 15))
                window.after(2000, menu_admin(window))
        else:
            mensaje_label.config(text="Nombre de usuario o contraseña incorrectos.", font=("sans-serif", 15))

    def menu_admin(window):
        for widget in window.winfo_children():
            widget.destroy()

        admin_label = tk.Label(window, text="Menú de Administrador", font=("sans-serif", 15))
        admin_label.pack(pady=20)

        opc1 = tk.Button(window, text="1. Crear cuenta Caja", font=("sans-serif", 15))
        opc1.pack(pady=10)

        opc2 = tk.Button(window, text="2. Crear cuenta Chef", font=("sans-serif", 15))
        opc2.pack(pady=10)

        opc3 = tk.Button(window, text="3. Crear cuenta Panel", font=("sans-serif", 15))
        opc3.pack(pady=10)

        opc4 = tk.Button(window, text="4. Establecer número de mesas", font=("sans-serif", 15))
        opc4.pack(pady=10)

        salir_button = tk.Button(window, text="Salir", font=("sans-serif", 15), command=window.quit)
        salir_button.pack(pady=10)

    login_button = tk.Button(window, text="Iniciar sesión", font=("sans-serif", 15),
                             command=lambda: login_usuario(usuario_entry, pass_entry, mensaje_label, window))
    login_button.pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
