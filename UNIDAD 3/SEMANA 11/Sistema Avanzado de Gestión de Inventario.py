"""
Sistema Avanzado de Gestión de Inventario
=========================================

Requisitos cubiertos:
- POO: clases Producto e Inventario.
- Colecciones: dict para almacenamiento principal, set y dict para índices por nombre, listas/tuplas para vistas.
- Archivos: persistencia en JSON con manejo de excepciones, serialización/deserialización.
- Interfaz de usuario: menú en consola con opciones agregar/eliminar/actualizar/buscar/mostrar/guardar/salir.
- Código organizado y comentado.

Ejecutar:
    python inventory_system.py

Archivo de datos por defecto: inventory_data.json (en la misma carpeta)

Sugerencia para PyCharm:
- Crear un nuevo proyecto, añadir este archivo como `inventory_system.py` y ejecutar.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Optional, List, Set
import json
import os


# ---------------------------
# Dominio: Clase Producto
# ---------------------------
@dataclass
class Producto:
    """Representa un ítem del inventario.

    Atributos:
        id (str): Identificador único del producto.
        nombre (str): Nombre comercial del producto.
        cantidad (int): Stock disponible (>= 0).
        precio (float): Precio unitario (>= 0.0).
    """
    id: str
    nombre: str
    cantidad: int
    precio: float

    def __post_init__(self) -> None:
        # Normalizar datos básicos y validar.
        self.id = self.id.strip()
        self.nombre = self.nombre.strip()
        if not self.id:
            raise ValueError("El ID no puede estar vacío.")
        if not self.nombre:
            raise ValueError("El nombre no puede estar vacío.")
        if not isinstance(self.cantidad, int) or self.cantidad < 0:
            raise ValueError("La cantidad debe ser un entero >= 0.")
        if not isinstance(self.precio, (int, float)) or self.precio < 0:
            raise ValueError("El precio debe ser un número >= 0.")

    # Getters/Setters explícitos (además de dataclass) para transparencia en POO
    def set_cantidad(self, nueva_cantidad: int) -> None:
        if nueva_cantidad < 0:
            raise ValueError("La cantidad no puede ser negativa.")
        self.cantidad = int(nueva_cantidad)

    def set_precio(self, nuevo_precio: float) -> None:
        if nuevo_precio < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.precio = float(nuevo_precio)

    def to_dict(self) -> Dict:
        return asdict(self)

    @staticmethod
    def from_dict(data: Dict) -> "Producto":
        return Producto(
            id=str(data["id"]),
            nombre=str(data["nombre"]),
            cantidad=int(data["cantidad"]),
            precio=float(data["precio"]),
        )


# ---------------------------
# Infraestructura: Inventario (colecciones + persistencia)
# ---------------------------
class Inventario:
    """Gestiona un conjunto de Productos usando colecciones eficientes.

    Estructuras internas:
        - _items: Dict[str, Producto] -> acceso O(1) por ID.
        - _index_nombre: Dict[str, Set[str]] -> índice invertido nombre->IDs para búsquedas rápidas por nombre.
    """

    def __init__(self) -> None:
        self._items: Dict[str, Producto] = {}
        self._index_nombre: Dict[str, Set[str]] = {}

    # ------------------ Operaciones CRUD ------------------
    def agregar(self, p: Producto) -> None:
        if p.id in self._items:
            raise KeyError(f"Ya existe un producto con ID {p.id}.")
        self._items[p.id] = p
        self._indexar_nombre(p)

    def eliminar(self, id_producto: str) -> Producto:
        id_producto = id_producto.strip()
        if id_producto not in self._items:
            raise KeyError(f"No existe producto con ID {id_producto}.")
        prod = self._items.pop(id_producto)
        self._desindexar_nombre(prod)
        return prod

    def actualizar_cantidad(self, id_producto: str, nueva_cantidad: int) -> None:
        prod = self._obtener_por_id(id_producto)
        prod.set_cantidad(nueva_cantidad)

    def actualizar_precio(self, id_producto: str, nuevo_precio: float) -> None:
        prod = self._obtener_por_id(id_producto)
        prod.set_precio(nuevo_precio)

    def buscar_por_nombre(self, termino: str) -> List[Producto]:
        """Búsqueda insensible a mayúsculas; coincide por nombre completo."""
        clave = termino.strip().lower()
        ids = self._index_nombre.get(clave, set())
        return [self._items[i] for i in ids]

    def listar_todos(self) -> List[Producto]:
        return list(self._items.values())

    def existe_id(self, id_producto: str) -> bool:
        return id_producto.strip() in self._items

    # ------------------ Persistencia en archivo ------------------
    def guardar_en_archivo(self, ruta: str) -> None:
        datos = [p.to_dict() for p in self.listar_todos()]
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise OSError(f"Error al guardar en '{ruta}': {e}")

    def cargar_de_archivo(self, ruta: str) -> None:
        if not os.path.exists(ruta):
            # Si no existe, iniciar limpio sin error.
            self._items.clear()
            self._index_nombre.clear()
            return
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("El archivo de datos está corrupto o no es JSON válido.")
        except OSError as e:
            raise OSError(f"Error al leer '{ruta}': {e}")

        # Reconstruir estructuras
        self._items.clear()
        self._index_nombre.clear()
        for entry in datos:
            p = Producto.from_dict(entry)
            self._items[p.id] = p
            self._indexar_nombre(p)

    # ------------------ Utilidades internas ------------------
    def _obtener_por_id(self, id_producto: str) -> Producto:
        id_producto = id_producto.strip()
        if id_producto not in self._items:
            raise KeyError(f"No existe producto con ID {id_producto}.")
        return self._items[id_producto]

    def _indexar_nombre(self, p: Producto) -> None:
        clave = p.nombre.lower()
        if clave not in self._index_nombre:
            self._index_nombre[clave] = set()
        self._index_nombre[clave].add(p.id)

    def _desindexar_nombre(self, p: Producto) -> None:
        clave = p.nombre.lower()
        ids = self._index_nombre.get(clave)
        if ids:
            ids.discard(p.id)
            if not ids:
                self._index_nombre.pop(clave, None)


# ---------------------------
# Interfaz de usuario (CLI)
# ---------------------------
ARCHIVO_DATOS_POR_DEFECTO = "inventory_data.json"

def _input_no_vacio(mensaje: str) -> str:
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("⚠ Entrada vacía, inténtalo de nuevo.")


def _input_entero(mensaje: str, minimo: Optional[int] = None) -> int:
    while True:
        raw = input(mensaje).strip()
        try:
            val = int(raw)
            if minimo is not None and val < minimo:
                print(f"⚠ Debe ser un entero >= {minimo}.")
                continue
            return val
        except ValueError:
            print("⚠ Ingresa un número entero válido.")


def _input_flotante(mensaje: str, minimo: Optional[float] = None) -> float:
    while True:
        raw = input(mensaje).strip()
        try:
            val = float(raw)
            if minimo is not None and val < minimo:
                print(f"⚠ Debe ser un número >= {minimo}.")
                continue
            return val
        except ValueError:
            print("⚠ Ingresa un número válido (usa punto decimal).")


def mostrar_producto(p: Producto) -> None:
    print(f"ID: {p.id} | Nombre: {p.nombre} | Cantidad: {p.cantidad} | Precio: {p.precio:.2f}")


def menu() -> None:
    inv = Inventario()

    # Cargar datos iniciales
    try:
        inv.cargar_de_archivo(ARCHIVO_DATOS_POR_DEFECTO)
        print(f"✔ Datos cargados de '{ARCHIVO_DATOS_POR_DEFECTO}'.")
    except Exception as e:
        print(f"⚠ No se pudieron cargar datos: {e}\nSe iniciará un inventario vacío.")

    while True:
        print("\n==== Menú Inventario ====")
        print("1) Añadir producto")
        print("2) Eliminar producto por ID")
        print("3) Actualizar cantidad")
        print("4) Actualizar precio")
        print("5) Buscar por nombre")
        print("6) Mostrar todos")
        print("7) Guardar en archivo")
        print("8) Salir")

        opcion = _input_no_vacio("Elige una opción (1-8): ")

        try:
            if opcion == "1":
                idp = _input_no_vacio("ID: ")
                if inv.existe_id(idp):
                    print("⚠ Ya existe ese ID. Operación cancelada.")
                    continue
                nombre = _input_no_vacio("Nombre: ")
                cantidad = _input_entero("Cantidad (>=0): ", minimo=0)
                precio = _input_flotante("Precio (>=0): ", minimo=0.0)
                inv.agregar(Producto(id=idp, nombre=nombre, cantidad=cantidad, precio=precio))
                inv.guardar_en_archivo(ARCHIVO_DATOS_POR_DEFECTO)  # autosave
                print("✔ Producto añadido y guardado.")

            elif opcion == "2":
                idp = _input_no_vacio("ID a eliminar: ")
                prod = inv.eliminar(idp)
                inv.guardar_en_archivo(ARCHIVO_DATOS_POR_DEFECTO)
                print("✔ Eliminado:")
                mostrar_producto(prod)

            elif opcion == "3":
                idp = _input_no_vacio("ID a actualizar cantidad: ")
                nueva = _input_entero("Nueva cantidad (>=0): ", minimo=0)
                inv.actualizar_cantidad(idp, nueva)
                inv.guardar_en_archivo(ARCHIVO_DATOS_POR_DEFECTO)
                print("✔ Cantidad actualizada.")

            elif opcion == "4":
                idp = _input_no_vacio("ID a actualizar precio: ")
                nuevo = _input_flotante("Nuevo precio (>=0): ", minimo=0.0)
                inv.actualizar_precio(idp, nuevo)
                inv.guardar_en_archivo(ARCHIVO_DATOS_POR_DEFECTO)
                print("✔ Precio actualizado.")

            elif opcion == "5":
                termino = _input_no_vacio("Nombre exacto a buscar: ")
                resultados = inv.buscar_por_nombre(termino)
                if not resultados:
                    print("(sin resultados)")
                else:
                    for p in resultados:
                        mostrar_producto(p)

            elif opcion == "6":
                productos = inv.listar_todos()
                if not productos:
                    print("(inventario vacío)")
                else:
                    # Orden estable por nombre y luego ID para lectura más cómoda
                    for p in sorted(productos, key=lambda x: (x.nombre.lower(), x.id)):
                        mostrar_producto(p)

            elif opcion == "7":
                ruta = input(f"Ruta (Enter = {ARCHIVO_DATOS_POR_DEFECTO}): ").strip() or ARCHIVO_DATOS_POR_DEFECTO
                inv.guardar_en_archivo(ruta)
                print(f"✔ Guardado en '{ruta}'.")

            elif opcion == "8":
                # Guardado final
                try:
                    inv.guardar_en_archivo(ARCHIVO_DATOS_POR_DEFECTO)
                    print(f"✔ Cambios guardados en '{ARCHIVO_DATOS_POR_DEFECTO}'.")
                except Exception as e:
                    print(f"⚠ No se pudo guardar automáticamente: {e}")
                print("👋 Saliendo...")
                break

            else:
                print("⚠ Opción inválida. Elige entre 1 y 8.")

        except (ValueError, KeyError) as e:
            # Errores de validación o claves inexistentes
            print(f"⚠ Error: {e}")
        except OSError as e:
            # Errores de E/S de archivos
            print(f"⚠ Error de archivo: {e}")
        except Exception as e:
            # Cualquier otro error inesperado
            print(f"⚠ Ocurrió un error inesperado: {e}")


# Punto de entrada
if __name__ == "__main__":
    menu()
