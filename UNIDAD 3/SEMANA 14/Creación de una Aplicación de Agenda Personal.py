"""
Agenda personal con GUI usando Tkinter
Archivo: agenda_tkinter.py
Requisitos cubiertos:
- Interfaz con Treeview mostrando fecha, hora y descripción
- Entradas para fecha (DatePicker con tkcalendar si está disponible), hora y descripción
- Botones: Agregar Evento, Eliminar Evento Seleccionado, Salir
- Confirmación al eliminar (opcional activada)
- Organización con Frames
- Persistencia simple en archivo JSON (events.json)
- Comentarios explicativos para cada parte

Para ejecutar:
- Recomiendo crear un entorno virtual
- pip install tkcalendar (opcional, si no se instala se usa entrada de texto para fecha)
- python agenda_tkinter.py

Autor: Johanna Gamboa — código original, personalizable
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Intentar importar DateEntry de tkcalendar para un DatePicker más amigable
try:
    from tkcalendar import DateEntry
    TKCALENDAR_AVAILABLE = True
except Exception:
    TKCALENDAR_AVAILABLE = False

EVENTS_FILE = "events.json"


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda Personal")
        self.geometry("700x450")
        self.resizable(False, False)

        # Cargar eventos (persistencia simple)
        self.events = self.load_events()

        # Configurar el layout principal: 3 frames
        self.create_frames()
        # Crear widgets dentro de los frames
        self.create_event_list()
        self.create_entry_fields()
        self.create_action_buttons()

        # Rellenar la lista con los eventos cargados
        self.refresh_treeview()

    def create_frames(self):
        # Frame superior: lista de eventos
        self.frame_list = ttk.Frame(self, padding=10)
        self.frame_list.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Frame medio: campos de entrada
        self.frame_inputs = ttk.Frame(self, padding=(10, 0))
        self.frame_inputs.pack(side=tk.TOP, fill=tk.X)

        # Frame inferior: botones de acción
        self.frame_actions = ttk.Frame(self, padding=10)
        self.frame_actions.pack(side=tk.BOTTOM, fill=tk.X)

    def create_event_list(self):
        # Treeview con columnas: ID (oculto), Fecha, Hora, Descripción
        columns = ("fecha", "hora", "descripcion")
        self.tree = ttk.Treeview(self.frame_list, columns=columns, show="headings", height=10)
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("descripcion", text="Descripción")

        # Ajustes de ancho
        self.tree.column("fecha", width=120, anchor=tk.CENTER)
        self.tree.column("hora", width=80, anchor=tk.CENTER)
        self.tree.column("descripcion", width=420, anchor=tk.W)

        # Barra de desplazamiento vertical
        vsb = ttk.Scrollbar(self.frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Evento doble click: mostrar detalle o editar (extensible)
        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def create_entry_fields(self):
        # Labels y entradas organizadas con grid dentro del frame_inputs
        # Fecha
        ttk.Label(self.frame_inputs, text="Fecha:").grid(row=0, column=0, padx=5, pady=8, sticky=tk.W)
        if TKCALENDAR_AVAILABLE:
            self.entry_fecha = DateEntry(self.frame_inputs, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        else:
            # Fallback: Entry con formato AAAA-MM-DD
            self.entry_fecha = ttk.Entry(self.frame_inputs)
            self.entry_fecha.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.entry_fecha.grid(row=0, column=1, padx=5, pady=8, sticky=tk.W)

        # Hora
        ttk.Label(self.frame_inputs, text="Hora (HH:MM):").grid(row=0, column=2, padx=5, pady=8, sticky=tk.W)
        self.entry_hora = ttk.Entry(self.frame_inputs, width=10)
        self.entry_hora.insert(0, datetime.now().strftime("%H:%M"))
        self.entry_hora.grid(row=0, column=3, padx=5, pady=8, sticky=tk.W)

        # Descripción
        ttk.Label(self.frame_inputs, text="Descripción:").grid(row=1, column=0, padx=5, pady=8, sticky=tk.W)
        self.entry_descripcion = ttk.Entry(self.frame_inputs, width=60)
        self.entry_descripcion.grid(row=1, column=1, columnspan=3, padx=5, pady=8, sticky=tk.W)

    def create_action_buttons(self):
        # Botones: Agregar, Eliminar, Salir
        btn_add = ttk.Button(self.frame_actions, text="Agregar Evento", command=self.add_event)
        btn_delete = ttk.Button(self.frame_actions, text="Eliminar Evento Seleccionado", command=self.delete_selected_event)
        btn_exit = ttk.Button(self.frame_actions, text="Salir", command=self.on_exit)

        # Empaquetado con padding
        btn_add.pack(side=tk.LEFT, padx=10, pady=6)
        btn_delete.pack(side=tk.LEFT, padx=10, pady=6)
        btn_exit.pack(side=tk.RIGHT, padx=10, pady=6)

    # ----------------- Manejo de eventos -----------------
    def add_event(self):
        # Leer campos
        fecha = self.get_fecha_text()
        hora = self.entry_hora.get().strip()
        descripcion = self.entry_descripcion.get().strip()

        # Validaciones básicas
        if not fecha:
            messagebox.showwarning("Fecha inválida", "Por favor ingrese una fecha válida (AAAA-MM-DD).")
            return
        if not self.validar_hora(hora):
            messagebox.showwarning("Hora inválida", "Ingrese la hora en formato HH:MM, por ejemplo 09:30.")
            return
        if not descripcion:
            messagebox.showwarning("Descripción vacía", "La descripción no puede estar vacía.")
            return

        # Crear un ID simple basado en timestamp
        event_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
        evento = {"id": event_id, "fecha": fecha, "hora": hora, "descripcion": descripcion}

        # Añadir a la lista interna y persistir
        self.events.append(evento)
        self.save_events()

        # Actualizar Treeview
        self.refresh_treeview()

        # Limpiar campos de descripción (mantener fecha y hora para rapidez)
        self.entry_descripcion.delete(0, tk.END)

    def delete_selected_event(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Seleccionar evento", "Seleccione primero un evento para eliminar.")
            return

        # Tomar el primer seleccionado
        item = selected[0]
        values = self.tree.item(item, "values")
        fecha, hora, descripcion = values

        # Confirmación
        confirm = messagebox.askyesno("Confirmar eliminación", f"¿Eliminar el evento:\n{fecha} {hora} - {descripcion}?")
        if not confirm:
            return

        # Buscar y eliminar por coincidencia exacta (fecha, hora, descripcion)
        for ev in list(self.events):
            if ev["fecha"] == fecha and ev["hora"] == hora and ev["descripcion"] == descripcion:
                self.events.remove(ev)
                break

        self.save_events()
        self.refresh_treeview()

    def on_tree_double_click(self, event):
        # Mostrar detalle simple en un diálogo (extensible para edición)
        item = self.tree.focus()
        if not item:
            return
        fecha, hora, descripcion = self.tree.item(item, "values")
        messagebox.showinfo("Detalle del evento", f"Fecha: {fecha}\nHora: {hora}\nDescripción: {descripcion}")

    def on_exit(self):
        # Pedir confirmación antes de salir
        if messagebox.askokcancel("Salir", "¿Está seguro que desea salir? Los cambios ya están guardados automáticamente."):
            self.destroy()

    # ----------------- Utilidades -----------------
    def refresh_treeview(self):
        # Limpiar
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Ordenar eventos por fecha + hora antes de mostrar
        def key_fn(ev):
            try:
                return datetime.strptime(ev['fecha'] + ' ' + ev['hora'], '%Y-%m-%d %H:%M')
            except Exception:
                return datetime.max

        for ev in sorted(self.events, key=key_fn):
            self.tree.insert('', tk.END, values=(ev['fecha'], ev['hora'], ev['descripcion']))

    def validar_hora(self, hora_text):
        try:
            datetime.strptime(hora_text, "%H:%M")
            return True
        except Exception:
            return False

    def get_fecha_text(self):
        # Si usamos DateEntry devuelve objeto con get_date o get_text dependiendo de la versión
        if TKCALENDAR_AVAILABLE:
            try:
                return self.entry_fecha.get_date().strftime('%Y-%m-%d')
            except Exception:
                try:
                    return self.entry_fecha.get()
                except Exception:
                    return None
        else:
            text = self.entry_fecha.get().strip()
            # Validar formato AAAA-MM-DD
            try:
                datetime.strptime(text, '%Y-%m-%d')
                return text
            except Exception:
                return None

    # ----------------- Persistencia -----------------
    def load_events(self):
        if not os.path.exists(EVENTS_FILE):
            return []
        try:
            with open(EVENTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
                return []
        except Exception:
            return []

    def save_events(self):
        try:
            with open(EVENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Error guardando", f"No se pudo guardar los eventos:\n{e}")


if __name__ == '__main__':
    app = AgendaApp()
    app.mainloop()
