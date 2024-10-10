import tkinter as tk
from controllers.admin_controller import AdminController  # Asegúrate de que el controlador esté importado

class AdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Administración")
        self.root.geometry("1200x600")
        self.controller = AdminController()  # Instancia del controlador
        self.create_interface()

    def create_interface(self):
        # Fondo blanco para toda la ventana
        self.root.configure(bg="white")

        # Cuadro ovalado vacío en la mitad derecha
        right_frame = tk.Frame(self.root, bg="lightgray", bd=5, relief="groove")
        right_frame.place(relx=0.74, rely=0.5, anchor="center", width=450, height=500)

        # Contenedor en la parte izquierda para gestionar el número de mesas
        left_frame = tk.Frame(self.root, bg="white")
        left_frame.place(relx=0.25, rely=0.5, anchor="center", width=300, height=500)

        # Área para gestionar el número de mesas
        tk.Label(left_frame, text="NÚMERO DE MESAS", font=("Arial", 16), bg="white").pack(pady=(20, 10))

        # Contenedor para los botones + y -
        number_frame = tk.Frame(left_frame, bg="white")
        number_frame.pack(pady=10)

        # Botón para disminuir el número de mesas
        self.decrease_button = tk.Button(number_frame, text="-", width=8, height=2, font=("Arial", 14), command=self.decrease_number)
        self.decrease_button.grid(row=0, column=0)

        # Cuadro de entrada para el número de mesas
        self.number_entry = tk.Entry(number_frame, width=10, font=("Arial", 14))
        self.number_entry.grid(row=0, column=1)
        self.number_entry.insert(0, "0")  # Valor inicial

        # Botón para aumentar el número de mesas
        self.increase_button = tk.Button(number_frame, text="+", width=8, height=2, font=("Arial", 14), command=self.increase_number)
        self.increase_button.grid(row=0, column=2)

        # Botón para aceptar el número de mesas
        accept_button = tk.Button(left_frame, text="ACEPTAR", width=35, height=2, font=("Arial", 14), command=self.create_mesas)
        accept_button.pack(pady=10)

        # Botones para crear cuentas con un tamaño mayor y centrados
        button1 = tk.Button(left_frame, text="CREAR CUENTA CHEF", width=35, height=2, font=("Arial", 14), command=lambda: self.create_user('chef'))
        button1.pack(pady=10)

        button2 = tk.Button(left_frame, text="CREAR CUENTA CAJA", width=35, height=2, font=("Arial", 14), command=lambda: self.create_user('caja'))
        button2.pack(pady=10)

        button3 = tk.Button(left_frame, text="CREAR CUENTA PANEL", width=35, height=2, font=("Arial", 14), command=lambda: self.create_user('panel'))
        button3.pack(pady=10)

        # Label para mostrar la información de las cuentas creadas
        self.result_label = tk.Label(right_frame, text="", font=("Arial", 14), bg="lightgray")
        self.result_label.pack(pady=20)

    def create_user(self, role):
        result = self.controller.create_user(role)
        if "error" in result:
            self.result_label.config(text=result["error"])
        else:
            self.result_label.config(text=f"Usuario: {result['username']}, Contraseña: {result['password']}")

    def create_mesas(self):
        try:
            num_mesas = int(self.number_entry.get())
            if num_mesas <= 0:
                raise ValueError("El número de mesas debe ser mayor que cero.")
            result = self.controller.create_mesas(num_mesas)
            self.result_label.config(text=result)
        except ValueError as e:
            self.result_label.config(text=str(e))

    def increase_number(self):
        current_value = int(self.number_entry.get())
        self.number_entry.delete(0, tk.END)
        self.number_entry.insert(0, str(current_value + 1))

    def decrease_number(self):
        current_value = int(self.number_entry.get())
        if current_value > 0:  # Evitar números negativos
            self.number_entry.delete(0, tk.END)
            self.number_entry.insert(0, str(current_value - 1))

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminView(root)
    root.mainloop()
