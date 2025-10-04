# main_gui.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from inventory import Inventario
from inventory import Producto

ARCHIVO_INVENTARIO = "inventario.json"

class App:
    def __init__(self, root):
        self.root = root
        root.title("Sistema de Inventario - POO")
        root.geometry("800x500")
        self.inventario = Inventario()
        self.inventario.cargar_desde_archivo(ARCHIVO_INVENTARIO)

        self._crear_menu()
        self._crear_pantalla_principal()
        # Atajos
        root.bind("<Escape>", lambda e: root.quit())

    def _crear_menu(self):
        menubar = tk.Menu(self.root)
        productos_menu = tk.Menu(menubar, tearoff=0)
        productos_menu.add_command(label="Gestionar Productos", command=self.abrir_ventana_productos)
        productos_menu.add_separator()
        productos_menu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Productos", menu=productos_menu)
        self.root.config(menu=menubar)

    def _crear_pantalla_principal(self):
        frame = ttk.Frame(self.root, padding=12)
        frame.pack(fill="both", expand=True)

        # Información del estudiante: edítala según corresponda
        estudiante_info = (
            "Estudiante: Johanna Gamboa\n"
            "Carrera: Ingeniería en Tecnologías de la Información\n"
            "Paralelo: A\n"
            "Asignatura: Programación Orientada a Objetos\n"
        )
        lbl_info = ttk.Label(frame, text=estudiante_info, justify="left", font=("Arial", 11))
        lbl_info.pack(anchor="nw")

        instrucciones = ("Menú -> Productos -> Gestionar Productos\n"
                          "Atajos: Delete = Eliminar producto seleccionado | Escape = Salir")
        ttk.Label(frame, text=instrucciones, padding=(0,10)).pack(anchor="nw")

    def abrir_ventana_productos(self):
        vp = tk.Toplevel(self.root)
        vp.title("Productos")
        vp.geometry("760x420")
        vp.transient(self.root)

        # Formulario de entrada
        form = ttk.Frame(vp, padding=8)
        form.pack(side="top", fill="x")

        ttk.Label(form, text="ID:").grid(row=0, column=0, sticky="e")
        id_entry = ttk.Entry(form, width=15)
        id_entry.grid(row=0, column=1, padx=4, pady=2)

        ttk.Label(form, text="Nombre:").grid(row=0, column=2, sticky="e")
        nombre_entry = ttk.Entry(form, width=30)
        nombre_entry.grid(row=0, column=3, padx=4, pady=2)

        ttk.Label(form, text="Cantidad:").grid(row=1, column=0, sticky="e")
        cantidad_entry = ttk.Entry(form, width=15)
        cantidad_entry.grid(row=1, column=1, padx=4, pady=2)

        ttk.Label(form, text="Precio:").grid(row=1, column=2, sticky="e")
        precio_entry = ttk.Entry(form, width=15)
        precio_entry.grid(row=1, column=3, padx=4, pady=2)

        # Botones
        botones = ttk.Frame(vp, padding=6)
        botones.pack(side="top", fill="x")

        def limpiar_form():
            id_entry.delete(0, tk.END)
            nombre_entry.delete(0, tk.END)
            cantidad_entry.delete(0, tk.END)
            precio_entry.delete(0, tk.END)

        def agregar():
            id_ = id_entry.get().strip()
            nombre = nombre_entry.get().strip()
            cantidad = cantidad_entry.get().strip()
            precio = precio_entry.get().strip()
            if not id_ or not nombre or not cantidad or not precio:
                messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
                return
            try:
                producto = Producto(id_, nombre, int(cantidad), float(precio))
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser entero y precio número.")
                return
            ok = self.inventario.agregar_producto(producto)
            if not ok:
                messagebox.showerror("Error", f"El ID {id_} ya existe.")
                return
            self._refrescar_tree(tree)
            self.inventario.guardar_en_archivo(ARCHIVO_INVENTARIO)
            limpiar_form()

        def modificar():
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("Info", "Seleccione un producto para modificar.")
                return
            id_ = id_entry.get().strip()
            nombre = nombre_entry.get().strip()
            cantidad = cantidad_entry.get().strip()
            precio = precio_entry.get().strip()
            if not id_ or not nombre or not cantidad or not precio:
                messagebox.showwarning("Validación", "Todos los campos son obligatorios.")
                return
            try:
                ok = self.inventario.modificar_producto(id_, nombre, int(cantidad), float(precio))
            except ValueError:
                messagebox.showerror("Error", "Cantidad debe ser entero y precio número.")
                return
            if not ok:
                messagebox.showerror("Error", f"No existe producto con ID {id_}.")
                return
            self._refrescar_tree(tree)
            self.inventario.guardar_en_archivo(ARCHIVO_INVENTARIO)
            limpiar_form()

        def eliminar(seleccion_manual=False):
            selected = tree.selection()
            if not selected:
                if not seleccion_manual:
                    return
                messagebox.showinfo("Info", "Seleccione un producto para eliminar.")
                return
            item = selected[0]
            id_ = tree.item(item, "values")[0]
            if messagebox.askyesno("Confirmar", f"Eliminar producto ID {id_}?"):
                self.inventario.eliminar_producto(id_)
                self._refrescar_tree(tree)
                self.inventario.guardar_en_archivo(ARCHIVO_INVENTARIO)

        ttk.Button(botones, text="Agregar", command=agregar).pack(side="left", padx=6)
        ttk.Button(botones, text="Modificar", command=modificar).pack(side="left", padx=6)
        ttk.Button(botones, text="Eliminar", command=lambda: eliminar(seleccion_manual=True)).pack(side="left", padx=6)
        ttk.Button(botones, text="Limpiar", command=limpiar_form).pack(side="left", padx=6)
        ttk.Button(botones, text="Cerrar", command=vp.destroy).pack(side="right", padx=6)

        # Treeview para listar productos
        cols = ("ID", "Nombre", "Cantidad", "Precio")
        tree = ttk.Treeview(vp, columns=cols, show="headings", selectmode="browse")
        for c in cols:
            tree.heading(c, text=c)
            # Ajustar ancho por columna
            if c == "Nombre":
                tree.column(c, width=300)
            else:
                tree.column(c, width=100, anchor="center")
        tree.pack(fill="both", expand=True, padx=6, pady=6)

        # Rellenar datos
        self._refrescar_tree(tree)

        # Eventos: al seleccionar, llenar el formulario
        def on_select(event):
            sel = tree.selection()
            if not sel:
                return
            item = sel[0]
            id_, nombre, cantidad, precio = tree.item(item, "values")
            id_entry.delete(0, tk.END); id_entry.insert(0, id_)
            nombre_entry.delete(0, tk.END); nombre_entry.insert(0, nombre)
            cantidad_entry.delete(0, tk.END); cantidad_entry.insert(0, cantidad)
            precio_entry.delete(0, tk.END); precio_entry.insert(0, precio)

        tree.bind("<<TreeviewSelect>>", on_select)
        # Atajo de teclado: tecla Delete para eliminar producto seleccionado
        tree.bind("<Delete>", lambda e: eliminar())

    def _refrescar_tree(self, tree):
        # limpiar
        for i in tree.get_children():
            tree.delete(i)
        for p in self.inventario.obtener_todos():
            tree.insert("", "end", values=(p.id, p.nombre, p.cantidad, f"{p.precio:.2f}"))

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
