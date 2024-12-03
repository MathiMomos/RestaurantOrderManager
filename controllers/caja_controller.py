from data.database import create_connection
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


class CajaController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_en_caja_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT orders.id, client.name, orders.items, orders.total, 'cliente' AS role
            FROM orders
            JOIN client ON orders.client_id = client.id
            WHERE orders.status = 'en caja'
        """)
        return cursor.fetchall()

    def generate_bill(self, order_id, method_pay, output_dir="."):
        cursor = self.conn.cursor()
        try:
            # Obtener información del pedidoa
            cursor.execute("""
                SELECT orders.id, client.name, orders.items, orders.item_prices, orders.item_amounts, orders.total
                FROM orders
                JOIN client ON orders.client_id = client.id
                WHERE orders.id = ?
            """, (order_id,))
            order = cursor.fetchone()

            if not order:
                print(f"No se encontró el pedido con ID {order_id}")
                return False

            order_id, cliente, platos, platos_precio, platos_cantidad, total = order

            # Limpiar las cadenas para eliminar las comas al final y separar los elementos
            platos = platos.strip(',').split(',')
            platos_precio = platos_precio.strip(',').split(',')
            platos_cantidad = platos_cantidad.strip(',').split(',')

            # Eliminar posibles valores vacíos de las listas
            platos = [p.strip() for p in platos if p.strip()]  # Eliminar platos vacíos
            platos_precio = [p.strip() for p in platos_precio if p.strip()]  # Eliminar precios vacíos
            platos_cantidad = [c.strip() for c in platos_cantidad if c.strip()]  # Eliminar cantidades vacías

            # Asegurarse de que los precios y las cantidades no estén vacíos y sean del tipo correcto
            platos_precio = [float(p) if p else 0.0 for p in platos_precio]  # Asignar 0.0 si el precio está vacío
            platos_cantidad = [int(c) if c else 0 for c in platos_cantidad]  # Asignar 0 si la cantidad está vacía

            # Generar archivo PDF
            pdf_file = self._generate_bill_pdf(order_id, cliente, platos, platos_precio, platos_cantidad, total,
                                               output_dir)

            # Registrar el pago en la base de datos
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                INSERT INTO caja (orders_id, method_pay)
                VALUES (?, ?)
            """, (order_id, method_pay))

            # Actualizar el estado del pedido
            cursor.execute("""
                UPDATE orders
                SET status = 'finalizado', time_out = ?
                WHERE id = ?
            """, (current_time, order_id))

            self.conn.commit()
            return pdf_file  # Retorna la ruta del archivo generado
        except Exception as e:
            print(f"Error al generar la boleta: {e}")
            self.conn.rollback()
            return False

    def _generate_bill_pdf(self, order_id, cliente, platos, platos_precio, platos_cantidad, total, output_dir="."):
        """
        Genera un archivo PDF para la boleta del pedido.

        :param order_id: ID del pedido.
        :param cliente: Nombre del cliente.
        :param platos: Lista de platos.
        :param platos_precio: Lista de precios correspondientes.
        :param platos_cantidad: Lista de cantidades correspondientes.
        :param total: Total de la cuenta.
        :param output_dir: Directorio donde se guardará el archivo PDF.
        :return: Ruta absoluta del archivo PDF generado.
        """
        # Crear el nombre del archivo
        pdf_file = os.path.join(output_dir, f"boleta_{order_id}.pdf")
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
        y_margin -= line_spacing * 2

        # Cabecera de la tabla de platos
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y_margin, "Plato")
        c.drawString(250, y_margin, "Cantidad")
        c.drawString(400, y_margin, "Precio (S/)")
        y_margin -= line_spacing

        # Línea separadora
        c.line(x_margin, y_margin, 550, y_margin)
        y_margin -= line_spacing

        # Detalles de los platos, cantidades y precios
        c.setFont("Helvetica", 12)
        for plato, precio, cantidad in zip(platos, platos_precio, platos_cantidad):
            # Verificar si el precio o cantidad está vacío o no es un número válido
            if not plato.strip() or not precio or not cantidad:
                continue  # Si el plato, precio o cantidad están vacíos, lo saltamos

            # Asegurarse de que el precio y la cantidad son del tipo adecuado
            try:
                precio = float(precio) if precio else 0.0  # Si el precio está vacío, lo asignamos como 0.0
            except ValueError:
                precio = 0.0  # Si el precio no es válido, asignamos 0.0

            try:
                cantidad = int(cantidad) if cantidad else 0  # Si la cantidad está vacía, la asignamos como 0
            except ValueError:
                cantidad = 0  # Si la cantidad no es válida, asignamos 0

            c.drawString(x_margin, y_margin, plato.strip())  # Eliminar espacios extra
            c.drawString(250, y_margin, str(cantidad))  # Mostrar la cantidad de forma correcta
            c.drawString(400, y_margin, f"S/ {float(precio * cantidad):.2f}")  # Calcular el total por item

            y_margin -= line_spacing

        # Línea separadora antes de los totales
        c.line(x_margin, y_margin, 550, y_margin)
        y_margin -= line_spacing * 2

        # Totales del pedido
        subtotal = total / 1.18
        igv = total - subtotal
        c.setFont("Helvetica", 12)
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
        return os.path.abspath(pdf_file)

    def process_panel_order(self, order_id):
        cursor = self.conn.cursor()
        try:
            # Solo actualizar si la cuenta es 'panel'
            cursor.execute("""
                UPDATE orders
                SET status = 'confirmado'
                WHERE id = ? AND client_id IN (
                    SELECT id FROM client WHERE id = orders.client_id
                )
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al procesar el pedido de panel: {e}")
            self.conn.rollback()
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()
