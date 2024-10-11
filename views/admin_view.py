import tkinter as tk
from controllers.admin_controller import AdminController

class AdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Administración")
        self.root.geometry("1200x600")
        self.controller = AdminController()
        self.create_interface()

    def create_interface(self):
        # Cambiar fondo de la ventana
        self.root.configure(bg="#DDD6CC")

        # Frame derecho
        right_frame = tk.Frame(self.root, bg="#19222B", bd=5, relief="groove")
        right_frame.place(relx=0.74, rely=0.5, anchor="center", width=450, height=500)

        # Frame izquierdo - aumentarlo considerablemente
        left_frame = tk.Frame(self.root, bg="#DDD6CC")
        left_frame.place(relx=0.25, rely=0.5, anchor="center", width=500, height=500)  # Ancho aumentado a 500

        # Frame para "Número de Mesas" y sus elementos (un único cuadro)
        number_frame = tk.Frame(left_frame, bg="#DDD6CC", bd=2, relief="solid", highlightbackground="#19222B", highlightthickness=1)
        number_frame.pack(pady=10, padx=10, ipadx=10)  # ipadx se puede ajustar si es necesario

        # Etiqueta de "Número de Mesas" con color actualizado
        tk.Label(number_frame, text="NÚMERO DE MESAS", font=("Arial", 16), bg="#DDD6CC", fg="#19222B").pack(pady=(10, 5))

        # Contenedor para el número y botones
        button_number_frame = tk.Frame(number_frame, bg="#DDD6CC")
        button_number_frame.pack(pady=5)

        # Botón disminuir
        self.decrease_button = tk.Button(button_number_frame, text="-", width=5, height=2, font=("Arial", 14), command=self.decrease_number,
                                         bg="#19222B", fg="#BD9240", activebackground="#19222B", activeforeground="#BD9240")
        self.decrease_button.grid(row=0, column=0)

        # Etiqueta para mostrar el número de mesas
        self.number_label = tk.Label(button_number_frame, width=5, font=("Arial", 14), bg="#DDD6CC", fg="#19222B", justify='center')
        self.number_label.grid(row=0, column=1)
        self.number_label.config(text="0")  # Inicializar con 0

        # Botón aumentar
        self.increase_button = tk.Button(button_number_frame, text="+", width=5, height=2, font=("Arial", 14), command=self.increase_number,
                                         bg="#19222B", fg="#BD9240", activebackground="#19222B", activeforeground="#BD9240")
        self.increase_button.grid(row=0, column=2)

        # Botón Aceptar
        accept_button = tk.Button(number_frame, text="ACEPTAR", width=35, height=2, font=("Arial", 14), command=self.create_mesas,
                                  bg="#19222B", fg="#BD9240", activebackground="#19222B", activeforeground="#BD9240")
        accept_button.pack(pady=10)

        # Botón Crear Cuenta Chef
        button1 = tk.Button(left_frame, text="CREAR CUENTA CHEF", width=35, height=2, font=("Arial", 14), command=lambda: self.create_user('chef'),
                            bg="#19222B", fg="#BD9240", activebackground="#19222B", activeforeground="#BD9240")
        button1.pack(pady=10)

        # Botón Crear Cuenta Caja
        button2 = tk.Button(left_frame, text="CREAR CUENTA CAJA", width=35, height=2, font=("Arial", 14), command=lambda: self.create_user('caja'),
                            bg="#19222B", fg="#BD9240", activebackground="#19222B", activeforeground="#BD9240")
        button2.pack(pady=10)

        # Botón Crear Cuenta Panel
        button3 = tk.Button(left_frame, text="CREAR CUENTA PANEL", width=35, height=2, font=("Arial", 14), command=lambda: self.create_user('panel'),
                            bg="#19222B", fg="#BD9240", activebackground="#19222B", activeforeground="#BD9240")
        button3.pack(pady=10)

        # Etiqueta para mostrar resultados
        self.result_label = tk.Label(right_frame, text="", font=("Arial", 14), bg="#19222B", fg="#BD9240")
        self.result_label.pack(pady=20)

    def create_user(self, role):
        result = self.controller.create_user(role)
        if "error" in result:
            self.result_label.config(text=result["error"])
        else:
            self.result_label.config(text=f"Usuario: {result['username']}, Contraseña: {result['password']}")

    def create_mesas(self):
        try:
            num_mesas = int(self.number_label['text'])  # Obtener el número de la etiqueta
            if num_mesas <= 0:
                raise ValueError("El número de mesas debe ser mayor que cero.")
            result = self.controller.create_mesas(num_mesas)
            self.result_label.config(text=result)
        except ValueError as e:
            self.result_label.config(text=str(e))

    def increase_number(self):
        current_value = int(self.number_label['text'])  # Obtener el número actual de la etiqueta
        self.number_label.config(text=str(current_value + 1))  # Actualizar el texto de la etiqueta

    def decrease_number(self):
        current_value = int(self.number_label['text'])  # Obtener el número actual de la etiqueta
        if current_value > 0:
            self.number_label.config(text=str(current_value - 1))  # Actualizar el texto de la etiqueta

if __name__ == "__main__":
    root = tk.Tk()
    app = AdminView(root)
    root.mainloop()
