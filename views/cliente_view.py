import tkinter as tk
from tkinter import messagebox, ttk
from controllers.cliente_controller import ClienteController
from PIL import Image, ImageTk

class ClienteView:

    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Cliente - Realizar Pedido")
        self.controller = ClienteController()
        self.user_id = user_id  # Aquí deberías recibir un string como "mesa1"
        self.client_id = 0
        self.mesa_id = 0
        self.current_order = None
        self.current_category = 0

        # Configuración de la ventana
        self.root.geometry("1280x720")  # Resolución fija de 1200x600
        self.root.resizable(False, False)  # Deshabilitar cambio de tamaño
        self.root.configure(bg="white")  # Fondo fuera del marco blanco

        # Crear un marco para los campos de entrada (20% más pequeño respecto al anterior)
        frame_width = 512  # 640 - 20%
        frame_height = 256  # 320 - 20%
        self.frame = tk.Frame(
            self.root,
            bg="#fafafa",  # Fondo más claro dentro del marco
            highlightbackground="#3b1d14",
            highlightthickness=2
        )
        self.frame.place(relx=0.5, rely=0.5, anchor="center", width=frame_width,
                         height=frame_height)  # Tamaño reducido y centrado

        # Etiqueta y entrada para el nombre
        self.name_label = tk.Label(self.frame, text="NOMBRE", font=("Arial", 12, "bold"), bg="#fafafa")
        self.name_label.place(relx=0.5, rely=0.2, anchor="center")  # Etiqueta centrada dentro del marco
        self.name_entry = tk.Entry(self.frame, width=30, font=("Arial", 12))
        self.name_entry.place(relx=0.5, rely=0.35, anchor="center")  # Entrada centrada justo debajo de la etiqueta

        # Etiqueta y entrada para el documento
        self.document_label = tk.Label(self.frame, text="DOCUMENTO", font=("Arial", 12, "bold"), bg="#fafafa")
        self.document_label.place(relx=0.5, rely=0.5, anchor="center")  # Etiqueta centrada dentro del marco
        self.document_entry = tk.Entry(self.frame, width=30, font=("Arial", 12))
        self.document_entry.place(relx=0.5, rely=0.65, anchor="center")  # Entrada centrada justo debajo de la etiqueta

        # Botón de envío dentro del marco
        self.submit_button = tk.Button(
            self.frame,
            text="INGRESAR",
            command=self.submit_person,
            font=("Arial", 12, "bold"),
            bg="#3b1d14",
            fg="white",
            activebackground="#5e2d20",
            activeforeground="white",
            padx=10,
            pady=5
        )
        self.submit_button.place(relx=0.5, rely=0.85, anchor="center")  # Botón centrado en la parte inferior del marco

        # Cargar y colocar las imágenes
        self.add_images()

    def add_images(self):
        try:
            # Cargar imágenes
            participa_img = Image.open("recursos/participa.png")
            participa_img = participa_img.resize((200, 200),
                                                 Image.Resampling.LANCZOS)  # Redimensionar con el método moderno
            self.participa_photo = ImageTk.PhotoImage(participa_img)

            cupones_img = Image.open("recursos/cupones.png")
            cupones_img = cupones_img.resize((200, 200),
                                             Image.Resampling.LANCZOS)  # Redimensionar con el método moderno
            self.cupones_photo = ImageTk.PhotoImage(cupones_img)

            # Crear widgets para las imágenes con ajustes en `relx`
            self.participa_label = tk.Label(self.root, image=self.participa_photo, bg="white")
            self.participa_label.place(relx=0.15, rely=0.5, anchor="center")  # Más a la izquierda

            self.cupones_label = tk.Label(self.root, image=self.cupones_photo, bg="white")
            self.cupones_label.place(relx=0.85, rely=0.5, anchor="center")  # Más a la derecha
        except Exception as e:
            print(f"Error al cargar las imágenes: {e}")

    def submit_person(self):
        name = self.name_entry.get()
        document = self.document_entry.get()

        if len(document) == 8:
            if name and document:
                # Verificar si el cliente ya está registrado en la base de datos
                existing_client = self.controller.get_client_by_document(document)

                if existing_client:
                    # El cliente ya está registrado
                    self.client_id = existing_client[0]
                    messagebox.showinfo("Bienvenido", f"Bienvenido de nuevo, {existing_client[1]}!")
                else:
                    # El cliente no está registrado, registrar en la base de datos
                    self.client_id = self.controller.add_new_client(name, document)
                    messagebox.showinfo("Bienvenido", f"Bienvenido, {name}! Tus datos han sido guardados.")

                # Limpiar los widgets de entrada y el botón antes de ir a la siguiente vista
                self.frame.destroy()

                # Llamar a la función para ir a la pantalla de órdenes
                self.ordenes_cliente(self.root, self.client_id, self.mesa_id)
            else:
                messagebox.showerror("Error", "Por favor, ingrese todos los datos.")
        else:
            messagebox.showerror("Error", "El DNI ingresado no es válido.")

    def ordenes_cliente(self, root, client_id, mesa_id):
        self.current_order = None
        self.current_category = 0


        # Configuración del fondo
        self.root.configure(bg="white")

        # Datos de los platos categorizados
        self.categories = ["SOPAS", "BEBIDAS", "PLATOS PRINCIPALES", "GUARNICIONES", "POSTRES", "ENTRADAS"]
        self.menu_items = {
            "SOPAS": [("Sopa a la Criolla", 18), ("Caldo de Gallina", 16), ("Chupe de Camarones", 22),
                      ("Shambar Norteño", 20), ("Sancochado", 24), ("Parihuela", 25), ("Sopa de Quinua", 15),
                      ("Sopa de Pollo", 17), ("Sopa de Verduras", 12)],
            "BEBIDAS": [("Chicha Morada", 8), ("Emoliente", 7), ("Refresco de Maracuyá", 7),
                        ("Jugo de Naranja", 10), ("Pisco Sour", 18), ("Cerveza Artesanal", 12), ("Agua Mineral", 5),
                        ("Café", 4), ("Té de Menta", 6)],
            "PLATOS PRINCIPALES": [("Lomo Saltado", 35), ("Ají de Gallina", 28), ("Seco de Res con Frejoles", 32),
                                   ("Tacu Tacu con Lomo", 38), ("Ceviche Mixto", 40), ("Arroz con Pollo", 30),
                                   ("Pollo a la Brasa", 25), ("Chicharrón de Pollo", 20), ("Parrillada", 45)],
            "GUARNICIONES": [("Arroz Blanco", 6), ("Papas Fritas", 10), ("Yuquitas Fritas", 12),
                             ("Ensalada Criolla", 10), ("Tostones de Plátano", 15), ("Arroz Chaufa", 18),
                             ("Puré de Papas", 8), ("Choclo con Queso", 7), ("Ensalada de Quinoa", 12)],
            "POSTRES": [("Suspiro a la Limeña", 15), ("Mazamorra Morada", 12), ("Arroz con Leche", 10),
                        ("Turrón de Doña Pepa", 18), ("Picarones", 20), ("Crema Volteada", 14),
                        ("Helado de Vainilla", 8), ("Tarta de Manzana", 12), ("Brownie con Helado", 14)],
            "ENTRADAS": [("Papa a la Huancaína", 15), ("Causa Rellena", 18), ("Anticuchos con Papas", 22),
                         ("Choclo con Queso", 14), ("Ocopa Arequipeña", 16), ("Tamales Criollos", 12),
                         ("Empanadas", 8), ("Tequeños", 10), ("Canastitas de Mariscos", 18)]
        }

        self.setup_ui()


    def setup_ui(self):
        # Frame izquierdo (vacío)
        self.left_frame = tk.Frame(self.root, bg="lightgray", width=310)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Frame derecho (contiene la funcionalidad)
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Botones de categorías en la parte superior del frame derecho
        self.category_buttons_frame = tk.Frame(self.right_frame, bg="white")
        self.category_buttons_frame.pack(pady=10)

        for category in self.categories:
            btn = tk.Button(
                self.category_buttons_frame,
                text=category,
                font=("Arial", 10, "bold"),
                bg="#3b1d14",  # Fondo colorido
                fg="white",  # Texto blanco
                height=2,
                width=17,
                relief="solid",
                command=lambda c=category: self.change_category(c)  # Cambiar categoría al hacer clic
            )
            btn.pack(side=tk.LEFT, padx=1)

        # Categoría de los platos
        self.label_category = tk.Label(
            self.right_frame,
            text=self.categories[self.current_category],
            font=("Arial", 24, "bold"),
            bg="white"
        )
        self.label_category.pack(pady=(20, 10))

        # Frame para los botones de los platos
        self.frame_menu = tk.Frame(self.right_frame, bg="white")
        self.frame_menu.pack(pady=(20, 30))

        self.create_menu_buttons()

        # Cargar el pedido actual automáticamente al iniciar
        self.show_order()  # Agrega esta línea

    def change_category(self, category):
        # Cambiar la categoría actual cuando se hace clic en una de ellas
        if category in self.categories:
            self.current_category = self.categories.index(category)
            self.update_category()

    def update_category(self):
        # Actualizar la categoría y mostrar los platos correspondientes
        self.label_category.config(text=self.categories[self.current_category])
        self.create_menu_buttons()

    def create_menu_buttons(self):
        # Limpiar el frame para evitar superposición de botones
        for widget in self.frame_menu.winfo_children():
            widget.destroy()

        # Crear botones para los platos de la categoría actual
        current_items = self.menu_items[self.categories[self.current_category]]
        row, col = 0, 0
        for idx, (plato, precio) in enumerate(current_items):
            btn = tk.Button(
                self.frame_menu,
                text=f"{plato}\nS/ {precio:.2f}",
                width=20,
                height=4,
                font=("Arial", 18),
                bg="white",
                fg="#3b1d14",
                highlightbackground="#3b1d14",
                highlightthickness=2,
                relief="solid",
                command=lambda p=plato, pr=precio: self.add_to_order(p, pr)
            )
            btn.grid(row=row, column=col, padx=20, pady=15)

            col += 1
            if col == 3:  # Solo tres botones por fila
                col = 0
                row += 1

        # Esto asegura que las filas y columnas tengan el mismo tamaño
        self.frame_menu.grid_rowconfigure(row, weight=1)
        self.frame_menu.grid_columnconfigure(0, weight=1)
        self.frame_menu.grid_columnconfigure(1, weight=1)
        self.frame_menu.grid_columnconfigure(2, weight=1)

    def add_to_order(self, plato, precio, cantidad=1):
        # Llamada al metodo de agregar ítem al pedido
        self.controller.add_item_to_order(self.user_id,self.client_id ,plato, precio, cantidad)
        self.load_current_order()

    def remove_selected_item(self):
        selected_item = self.tree_order.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un plato de la orden para eliminar.")
            return

        # Guardar la selección antes de realizar la eliminación
        selected_item_values = self.tree_order.item(selected_item, "values")

        # Obtener el plato seleccionado
        plato_seleccionado = selected_item_values[0]  # Nombre del plato

        # Llamar al metodo para eliminar el plato o decrementar la cantidad
        self.controller.remove_item_from_order(self.user_id, self.client_id, plato_seleccionado)

        # Recargar la orden actual después de la eliminación
        self.load_current_order()

        # Volver a seleccionar el plato que fue seleccionado previamente
        for item in self.tree_order.get_children():
            if self.tree_order.item(item, "values")[0] == plato_seleccionado:
                self.tree_order.selection_set(item)
                break

    def show_order(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Crear un estilo para el Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12))  # Cambiar el tamaño de la fuente para las celdas
        style.configure("Custom.Treeview.Heading",
                        font=("Arial", 13, "bold"))  # Cambiar el tamaño de la fuente para las cabeceras

        # Crear el Treeview con el estilo personalizado
        self.tree_order = ttk.Treeview(self.left_frame, columns=("Platos", "Precio", "Cantidad"), show='headings',
                                       style="Custom.Treeview")
        self.tree_order.heading("Platos", text="Platos")
        self.tree_order.heading("Precio", text="Prec/Uni")
        self.tree_order.heading("Cantidad", text="Cantidad")

        self.tree_order.column("Platos", width=200)  # Ancho de la columna Platos
        self.tree_order.column("Precio", width=80, anchor='center')  # Ancho de la columna Precio
        self.tree_order.column("Cantidad", width=80, anchor='center')  # Ancho de la columna Cantidad

        self.tree_order.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.load_current_order()

        self.button_confirm = tk.Button(
            self.left_frame,
            text="Confirmar Pedido",
            command=self.confirm_order,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14)
        )
        self.button_confirm.pack(side=tk.LEFT, padx=20, pady=20)

        # Botón para eliminar el plato seleccionado
        self.button_remove = tk.Button(
            self.left_frame,
            text="Eliminar Plato",
            command=self.remove_selected_item,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14)
        )
        self.button_remove.pack(side=tk.LEFT, padx=20, pady=20)

    def load_current_order(self):
        self.current_order = self.controller.get_current_order(self.user_id , self.client_id)
        for row in self.tree_order.get_children():
            self.tree_order.delete(row)
        if self.current_order:
            order_id, items, item_prices, item_amounts, total = self.current_order
            platos_lista = [plato.strip() for plato in items.split(',')]
            precios_lista = [float(precio.strip()) for precio in item_prices.split(',') if precio.strip()]
            cantidades_lista = [int(cantidad.strip()) for cantidad in item_amounts.split(',') if cantidad.strip()]
            for plato, precio, cantidad in zip(platos_lista, precios_lista, cantidades_lista):
                self.tree_order.insert("", tk.END, values=(plato, f"S/ {precio:.2f}", f"{cantidad}"))
            self.tree_order.insert("", tk.END, values=("Total", f"S/ {total:.2f}"))
        else:
            self.tree_order.insert("", tk.END, values=("No hay pedido actual.", "S/ 0.00"))

    def confirm_order(self):
        if self.current_order:
            order_id, items, item_prices, item_amounts, total = self.current_order
            confirm = messagebox.askyesno("Confirmar Pedido", f"¿Deseas confirmar tu pedido ID {order_id}?")
            if confirm:
                success = self.controller.confirm_order(order_id)
                if success:
                    messagebox.showinfo("Éxito", "Pedido confirmado y enviado al chef.")
                    self.load_current_order()
                else:
                    messagebox.showerror("Error", "No se pudo confirmar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "No tienes ningún pedido para confirmar.")