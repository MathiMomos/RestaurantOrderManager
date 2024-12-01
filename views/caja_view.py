import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Importar el controlador (asegúrate de que el archivo esté configurado correctamente)
from controllers.caja_controller import CajaController


class CajaView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Caja - Pedidos en Caja")
        self.controller = CajaController()
        self.user_id = user_id

        # Configuración de la interfaz
        self.root.configure(bg="#f7f7f7")

        # Etiqueta de título
        self.label = tk.Label(
            root,
            text="Pedidos en Caja",
            font=("Arial", 18, 'bold'),
            bg="#f7f7f7",
            fg="#3b1d14",
        )
        self.label.pack(pady=20)

        # Estilo del Treeview para mostrar los pedidos
        self.style = ttk.Style()
        self.style.configure(
            "Treeview",
            font=("Arial", 12),
            background="#f9f9f9",
            foreground="#3b1d14",
            rowheight=40,
        )
        self.style.configure(
            "Treeview.Heading",
            font=("Arial", 14, 'bold'),
            background="#f7f7f7",
            foreground="black",
        )
        self.style.map(
            "Treeview",
            background=[('selected', '#3b1d14')],
            foreground=[('selected', 'white')],
        )

        # Treeview para mostrar los pedidos
        self.tree = ttk.Treeview(
            root,
            columns=("ID", "Cliente", "Platos", "Total", "Tipo Cuenta"),
            show='headings',
            style="Treeview",
        )
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Platos", text="Platos")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Tipo Cuenta", text="Tipo Cuenta")
        self.tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame para botones
        button_frame = tk.Frame(root, bg="#f7f7f7")
        button_frame.pack(pady=10)

        # Botón para generar la boleta
        self.button_generate = tk.Button(
            button_frame,
            text="Generar Boleta (Clientes)",
            command=self.generate_selected_bill,
            width=25,
            height=2,
            font=("Arial", 12),
            bg="#3b1d14",
            fg="white",
            highlightbackground="#3b1d14",
            highlightthickness=2,
            relief="solid",
        )
        self.button_generate.pack(side=tk.LEFT, padx=10)

        # Botón para procesar pedidos de panel
        self.button_process_panel = tk.Button(
            button_frame,
            text="Procesar Pedido de Panel",
            command=self.process_selected_panel_order,
            width=25,
            height=2,
            font=("Arial", 12),
            bg="#3b1d14",
            fg="white",
            highlightbackground="#3b1d14",
            highlightthickness=2,
            relief="solid",
        )
        self.button_process_panel.pack(side=tk.LEFT, padx=10)

        self.load_orders()

    def load_orders(self):
        """Cargar los pedidos en la caja"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.controller.get_en_caja_orders()
        for order in orders:
            self.tree.insert("", tk.END, values=order)

    def generate_selected_bill(self):
        """Generar la boleta para el pedido seleccionado y mostrarla"""
        selected = self.tree.focus()
        if selected:
            order = self.tree.item(selected, 'values')
            order_id = order[0]
            cliente = order[1]
            platos = order[2]
            total = float(order[3])
            tipo_cuenta = order[4]

            if tipo_cuenta == 'cliente':
                confirm = messagebox.askyesno(
                    "Generar Boleta",
                    f"¿Deseas generar la boleta para el pedido ID {order_id} de {cliente}?"
                )
                if confirm:
                    # Crear el archivo PDF
                    pdf_file = f"boleta_{order_id}.pdf"
                    c = canvas.Canvas(pdf_file, pagesize=letter)

                    # Configurar márgenes y posiciones iniciales
                    x_margin = 50
                    y_margin = 750
                    line_spacing = 20

                    # Encabezado del restaurante
                    c.setFont("Helvetica-Bold", 16)
                    c.drawCentredString(300, y_margin, "EL CRIOLLITO RESTAURANT")
                    y_margin -= line_spacing
                    c.setFont("Helvetica", 12)
                    c.drawCentredString(300, y_margin, "JR. Paz Soldán Mza. B Lote 6, Urb. Obreros Municipales Puente")
                    y_margin -= line_spacing
                    c.drawCentredString(300, y_margin, "Santa Rosa - Mollendo - Arequipa")
                    y_margin -= line_spacing
                    c.drawCentredString(300, y_margin, "RUC: 10435353505")
                    y_margin -= line_spacing * 2

                    # Línea separadora
                    c.line(x_margin, y_margin, 550, y_margin)
                    y_margin -= line_spacing

                    # Información del cliente y pedido
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(x_margin, y_margin, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                    y_margin -= line_spacing
                    c.drawString(x_margin, y_margin, f"Cliente: {cliente}")
                    y_margin -= line_spacing
                    c.drawString(x_margin, y_margin, f"Pedido ID: {order_id}")
                    y_margin -= line_spacing
                    c.drawString(x_margin, y_margin, f"Platos: {platos}")
                    y_margin -= line_spacing * 2

                    # Totales del pedido
                    c.setFont("Helvetica", 12)
                    subtotal = total / 1.18
                    igv = total - subtotal
                    c.drawString(x_margin, y_margin, f"Subtotal: S/ {subtotal:.2f}")
                    y_margin -= line_spacing
                    c.drawString(x_margin, y_margin, f"IGV (18%): S/ {igv:.2f}")
                    y_margin -= line_spacing
                    c.setFont("Helvetica-Bold", 12)
                    c.drawString(x_margin, y_margin, f"Total: S/ {total:.2f}")
                    y_margin -= line_spacing * 2

                    # Mensaje de agradecimiento
                    c.setFont("Helvetica", 12)
                    c.drawCentredString(300, y_margin, "¡Gracias por su preferencia!")
                    y_margin -= line_spacing
                    c.line(x_margin, y_margin, 550, y_margin)

                    # Guardar el PDF
                    c.save()

                    # Mostrar mensaje de éxito
                    messagebox.showinfo("Éxito", f"Boleta generada correctamente: {pdf_file}")

                    # Mostrar el PDF en el visor predeterminado
                    abs_path = os.path.abspath(pdf_file)
                    os.startfile(abs_path)
            else:
                messagebox.showwarning("Advertencia", "Solo se puede generar boleta para pedidos de clientes.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para generar la boleta.")

    def process_selected_panel_order(self):
        """Procesar el pedido seleccionado desde el panel"""
        selected = self.tree.focus()
        if selected:
            order = self.tree.item(selected, 'values')
            order_id = order[0]
            # Lógica para procesar el pedido en el panel
            messagebox.showinfo("Procesar Pedido", f"Pedido ID {order_id} ha sido procesado.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para procesar.")




