# panel_view.py
import tkinter as tk
from tkinter import messagebox
from controllers.panel_controller import PanelController

class PanelView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Panel - Restaurant Order Manager")
        self.controller = PanelController()
        self.user_id = user_id

        # Configuración de la ventana
        self.root.configure(bg="white")
        self.root.geometry("800x600")  # Establece un tamaño inicial para la ventana

        # Espacio para la imagen
        self.image_frame = tk.Frame(self.root, bg="white", width=800, height=300)
        self.image_frame.pack(fill=tk.BOTH, expand=False)

        # Aquí puedes cargar una imagen si tienes el archivo correspondiente
        self.label_image = tk.Label(self.image_frame, text="Espacio para imagen", bg="white", font=("Arial", 18))
        self.label_image.pack(expand=True)

        # Botones principales
        self.buttons_frame = tk.Frame(self.root, bg="white")
        self.buttons_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Botón para mostrar mesas
        self.button_show_tables = tk.Button(
            self.buttons_frame,
            text="Mostrar Mesas",
            font=("Arial", 16, "bold"),
            bg="green",
            fg="white",
            command=self.show_tables
        )
        self.button_show_tables.grid(row=0, column=0, padx=20, pady=20)

        # Botón para pedir desde el panel
        self.button_manage_orders = tk.Button(
            self.buttons_frame,
            text="Pedir desde Panel",
            font=("Arial", 16, "bold"),
            bg="blue",
            fg="white",
            command=self.manage_orders  # Vacío por ahora
        )
        self.button_manage_orders.grid(row=0, column=1, padx=20, pady=20)

        # Botón para regresar a LoginView
        self.button_logout = tk.Button(
            self.buttons_frame,
            text="Cerrar Sesión",
            font=("Arial", 16, "bold"),
            bg="red",
            fg="white",
            command=self.logout
        )
        self.button_logout.grid(row=1, column=0, padx=20, pady=20)

    def show_tables(self):
        """Mostrar el estado de las mesas."""
        tables = self.controller.get_tables_data()  # Obtiene datos de la base de datos a través del controlador
        if not tables:
            messagebox.showwarning("Mesas", "No se encontraron mesas registradas.")
            return

        tables_window = tk.Toplevel(self.root)
        tables_window.title("Estado de las Mesas")
        tables_window.geometry("600x400")
        tables_window.configure(bg="white")

        # Mostrar las mesas con el estado apropiado
        for index, table in enumerate(tables):
            table_id, state = table  # Suponemos que 'state_table' es 0 (libre) o 1 (ocupada)
            color = "green" if state == 0 else "red"
            text = f"Mesa {table_id}: {'Libre' if state == 0 else 'Ocupada'}"

            button = tk.Button(
                tables_window,
                text=text,
                font=("Arial", 14),
                bg=color,
                fg="black",
                state="disabled"  # Deshabilitamos el botón ya que es solo para mostrar el estado
            )
            button.grid(row=index // 4, column=index % 4, padx=10, pady=10)

        # Cambiado de pack a grid para el botón de "Volver"
        back_button = tk.Button(tables_window, text="Volver", font=("Arial", 14), bg="gray", fg="white",
                                command=self.return_to_main)
        back_button.grid(row=len(tables) // 4 + 1, column=0, columnspan=4, pady=20)  # Alinea el botón al final

    def return_to_main(self):
        """Cerrar la ventana de mesas y regresar a la ventana principal."""
        self.root.deiconify()  # Mostrar la ventana principal nuevamente
        self.root.quit()  # Terminar la ejecución de la ventana secundaria

    def manage_orders(self):
        """Gestionar pedidos desde el panel."""
        # Este método está vacío por ahora, puedes implementar el flujo más adelante.
        pass

    def logout(self):
        """Cerrar la sesión y regresar a la ventana de login."""
        self.root.destroy()  # Cerrar la ventana actual (panel)

        # Importamos LoginView solo cuando se necesite
        from views.login_view import LoginView  # Importación local para evitar el ciclo de imports
        root = tk.Tk()  # Crear una nueva ventana para el login
        root.geometry("1200x600")
        LoginView(root)  # Llamar a la vista de login
        root.mainloop()  # Ejecutar la ventana de login
