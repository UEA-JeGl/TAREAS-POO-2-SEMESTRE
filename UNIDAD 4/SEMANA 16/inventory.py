# inventory.py
import json
from product import Producto
from typing import Dict, List

class Inventario:
    def __init__(self):
        # Almacenar productos en un dict por id para acceso rápido
        self.productos: Dict[str, Producto] = {}

    def agregar_producto(self, producto: Producto) -> bool:
        """Agrega un producto si no existe el ID. Retorna True si se agregó."""
        if producto.id in self.productos:
            return False
        self.productos[producto.id] = producto
        return True

    def eliminar_producto(self, id_: str) -> bool:
        """Elimina producto por ID. Retorna True si se eliminó."""
        if id_ in self.productos:
            del self.productos[id_]
            return True
        return False

    def modificar_producto(self, id_: str, nombre: str, cantidad: int, precio: float) -> bool:
        """Modifica un producto existente. Retorna True si se modificó."""
        if id_ in self.productos:
            p = self.productos[id_]
            p.nombre = nombre
            p.cantidad = int(cantidad)
            p.precio = float(precio)
            return True
        return False

    def obtener_todos(self) -> List[Producto]:
        return list(self.productos.values())

    def guardar_en_archivo(self, ruta: str):
        data = [p.to_dict() for p in self.obtener_todos()]
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def cargar_desde_archivo(self, ruta: str):
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.productos = {d["id"]: Producto.from_dict(d) for d in data}
        except FileNotFoundError:
            # Si no existe el archivo, iniciamos con inventario vacío
            self.productos = {}
        except Exception as e:
            # Si hay error en el archivo (formato), iniciamos vacío
            print(f"Error al cargar inventario: {e}")
            self.productos = {}
