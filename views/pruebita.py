import tkinter as tk

# Crear la ventana principal
root = tk.Tk()
root.title("Parte Scrolleable a la Izquierda y No Scrolleable a la Derecha")

# Crear un Canvas para la parte scrolleable
canvas = tk.Canvas(root, width=300, height=300)
canvas.pack(side="left", padx=10, pady=10)

# Crear una barra de desplazamiento para el Canvas
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side="left", fill="y")

# Configurar el Canvas para que use la barra de desplazamiento
canvas.config(yscrollcommand=scrollbar.set)

# Crear un Frame dentro del Canvas para contener los widgets desplazables
scrollable_frame = tk.Frame(canvas)

# Agregar el Frame dentro del Canvas
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

# Agregar contenido al Frame desplazable
for i in range(30):
    tk.Label(scrollable_frame, text=f"Elemento {i+1}").pack()

# Configurar el área de desplazamiento del Canvas
scrollable_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Crear el widget no desplazable a la derecha
tk.Label(root, text="Este es un widget no desplazable.").pack(side="right", padx=10, pady=10)

# Ejecutar la aplicación
root.mainloop()
