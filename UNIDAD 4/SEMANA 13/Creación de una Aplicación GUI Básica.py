import tkinter as tk
from tkinter import messagebox

# ------------------------
# Aplicación GUI con Tkinter
# ------------------------

def agregar_dato():
    """Toma el texto del campo de entrada y lo agrega a la lista si no está vacío."""
    texto = entrada.get().strip()
    if texto:
        lista_datos.insert(tk.END, texto)
        entrada.delete(0, tk.END)  # limpia el campo de texto
    else:
        messagebox.showwarning("Entrada vacía", "Por favor, ingrese un dato antes de agregar.")

def limpiar_datos():
    """Elimina el ítem seleccionado o toda la lista si no hay selección."""
    seleccion = lista_datos.curselection()
    if seleccion:
        lista_datos.delete(seleccion)
    else:
        lista_datos.delete(0, tk.END)

# ------------------------
# Configuración de la ventana principal
# ------------------------
ventana = tk.Tk()
ventana.title("Gestor de Datos Básico")
ventana.geometry("400x300")
ventana.resizable(False, False)

# ------------------------
# Componentes GUI
# ------------------------
# Etiqueta principal
etiqueta = tk.Label(ventana, text="Ingrese un dato y agréguelo a la lista:", font=("Arial", 12))
etiqueta.grid(row=0, column=0, columnspan=2, pady=10)

# Campo de texto
entrada = tk.Entry(ventana, width=30)
entrada.grid(row=1, column=0, padx=10, pady=5)

# Botón Agregar
btn_agregar = tk.Button(ventana, text="Agregar", command=agregar_dato)
btn_agregar.grid(row=1, column=1, padx=5, pady=5)

# Lista para mostrar datos
lista_datos = tk.Listbox(ventana, width=40, height=10)
lista_datos.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Botón Limpiar
btn_limpiar = tk.Button(ventana, text="Limpiar", command=limpiar_datos)
btn_limpiar.grid(row=3, column=0, columnspan=2, pady=10)

# ------------------------
# Bucle principal
# ------------------------
ventana.mainloop()

