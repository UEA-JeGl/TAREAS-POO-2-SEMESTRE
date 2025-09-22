import tkinter as tk
from tkinter import messagebox


class ListaTareasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista de Tareas")
        self.root.geometry("400x400")
        self.root.resizable(False, False)

        # Lista donde se almacenarán las tareas
        self.tareas = []

        # Campo de entrada para escribir nuevas tareas
        self.entrada_tarea = tk.Entry(root, width=35, font=("Arial", 12))
        self.entrada_tarea.pack(pady=10)

        # Permitir añadir con tecla ENTER
        self.entrada_tarea.bind("<Return>", self.agregar_tarea_evento)

        # Botones principales
        self.boton_agregar = tk.Button(root, text="Añadir Tarea", command=self.agregar_tarea)
        self.boton_agregar.pack(pady=5)

        self.boton_completar = tk.Button(root, text="Marcar como Completada", command=self.marcar_completada)
        self.boton_completar.pack(pady=5)

        self.boton_eliminar = tk.Button(root, text="Eliminar Tarea", command=self.eliminar_tarea)
        self.boton_eliminar.pack(pady=5)

        # Lista donde se muestran las tareas
        self.lista_tareas = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.lista_tareas.pack(pady=10)

        # Evento opcional: doble clic para marcar tarea como completada
        self.lista_tareas.bind("<Double-1>", self.marcar_completada_evento)

    # ------------------ Funciones de la lógica ------------------

    def agregar_tarea_evento(self, event):
        """Permite agregar una tarea presionando Enter."""
        self.agregar_tarea()

    def agregar_tarea(self):
        """Agrega la tarea escrita en el campo de entrada a la lista."""
        tarea = self.entrada_tarea.get().strip()
        if tarea:  # Solo se añade si no está vacío
            self.tareas.append(tarea)
            self.lista_tareas.insert(tk.END, tarea)
            self.entrada_tarea.delete(0, tk.END)  # Limpiar el campo de entrada
        else:
            messagebox.showwarning("Atención", "No se puede añadir una tarea vacía.")

    def marcar_completada_evento(self, event):
        """Permite marcar como completada con doble clic."""
        self.marcar_completada()

    def marcar_completada(self):
        """Cambia el estado de la tarea seleccionada a 'completada' visualmente."""
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            indice = seleccion[0]
            tarea = self.lista_tareas.get(indice)

            # Revisar si ya está marcada como completada
            if not tarea.startswith("[✔] "):
                tarea_completada = "[✔] " + tarea
                self.lista_tareas.delete(indice)
                self.lista_tareas.insert(indice, tarea_completada)
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para marcarla como completada.")

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada de la lista."""
        seleccion = self.lista_tareas.curselection()
        if seleccion:
            indice = seleccion[0]
            self.lista_tareas.delete(indice)
            del self.tareas[indice]
        else:
            messagebox.showinfo("Información", "Selecciona una tarea para eliminarla.")


# ------------------ Programa principal ------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = ListaTareasApp(root)
    root.mainloop()
