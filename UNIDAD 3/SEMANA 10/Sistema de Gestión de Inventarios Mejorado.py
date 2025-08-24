# -------------------------------------------------------
# Sistema de Gestión de Inventarios con Archivos
# Autor: [Johanna Gamboa]
# Descripción:
# Este programa implementa un sistema de gestión de inventarios
# para una tienda, utilizando Programación Orientada a Objetos.
# Además, almacena los productos en un archivo de texto y
# maneja excepciones en operaciones de lectura/escritura.
# -------------------------------------------------------

import os

# -----------------------
# Clase Producto
# -----------------------
class Producto:
    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """
        Constructor de la clase Producto.
        """
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def get_id(self):
        return self.id_producto

    def get_nombre(self):
        return self.nombre

    def set_nombre(self, nuevo_nombre: str):
        self.nombre = nuevo_nombre

    def get_cantidad(self):
        return self.cantidad

    def set_cantidad(self, nueva_cantidad: int):
        self.cantidad = nueva_cantidad

    def get_precio(self):
        return self.precio

    def set_precio(self, nuevo_precio: float):
        self.precio = nuevo_precio

    def __str__(self):
        """
        Representación en texto del producto.
        """
        return f"ID: {self.id_producto} | Nombre: {self.nombre} | Cantidad: {self.cantidad} | Precio: ${self.precio:.2f}"

    def to_line(self):
        """Convierte un producto a formato de línea para archivo."""
        return f"{self.id_producto},{self.nombre},{self.cantidad},{self.precio}\n"

    @staticmethod
    def from_line(linea: str):
        """Reconstruye un producto desde una línea de archivo."""
        try:
            partes = linea.strip().split(",")
            return Producto(int(partes[0]), partes[1], int(partes[2]), float(partes[3]))
        except (IndexError, ValueError):
            print("⚠️ Advertencia: línea de archivo corrupta, se omitirá:", linea.strip())
            return None


# -----------------------
# Clase Inventario
# -----------------------
class Inventario:
    def __init__(self, archivo="inventario.txt"):
        """
        Constructor: inicializa lista de productos y carga desde archivo.
        """
        self.productos = []
        self.archivo = archivo
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """Carga productos desde archivo al iniciar el programa."""
        if not os.path.exists(self.archivo):
            # Si el archivo no existe, lo creamos vacío
            try:
                open(self.archivo, "w").close()
            except PermissionError:
                print("❌ Error: no tienes permiso para crear el archivo de inventario.")
            return

        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    producto = Producto.from_line(linea)
                    if producto:
                        self.productos.append(producto)
        except FileNotFoundError:
            print("⚠️ Archivo de inventario no encontrado. Se creará uno nuevo.")
        except PermissionError:
            print("❌ No tienes permisos para leer el archivo de inventario.")

    def guardar_en_archivo(self):
        """Guarda todos los productos en el archivo."""
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                for p in self.productos:
                    f.write(p.to_line())
        except PermissionError:
            print("❌ Error: no tienes permiso para escribir en el archivo.")
        except Exception as e:
            print(f"❌ Error inesperado al guardar en archivo: {e}")

    def agregar_producto(self, producto: Producto):
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("❌ Error: Ya existe un producto con ese ID.")
                return
        self.productos.append(producto)
        self.guardar_en_archivo()
        print("✅ Producto agregado con éxito y guardado en archivo.")

    def eliminar_producto(self, id_producto: int):
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                self.guardar_en_archivo()
                print("✅ Producto eliminado del inventario y del archivo.")
                return
        print("❌ Error: No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto: int, nueva_cantidad=None, nuevo_precio=None):
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                self.guardar_en_archivo()
                print("✅ Producto actualizado en inventario y archivo.")
                return
        print("❌ Error: No se encontró un producto con ese ID.")

    def buscar_producto(self, nombre: str):
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("🔍 Resultados de la búsqueda:")
            for p in resultados:
                print(p)
        else:
            print("❌ No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        if not self.productos:
            print("📦 El inventario está vacío.")
        else:
            print("📋 Lista de productos en inventario:")
            for p in self.productos:
                print(p)


# -----------------------
# Interfaz de Usuario
# -----------------------
def menu():
    inventario = Inventario()

    while True:
        print("\n========= MENÚ INVENTARIO =========")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto por nombre")
        print("5. Mostrar todos los productos")
        print("6. Salir")
        print("===================================")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_producto = int(input("Ingrese ID del producto: "))
                nombre = input("Ingrese nombre del producto: ")
                cantidad = int(input("Ingrese cantidad: "))
                precio = float(input("Ingrese precio: "))
                nuevo = Producto(id_producto, nombre, cantidad, precio)
                inventario.agregar_producto(nuevo)
            except ValueError:
                print("❌ Error: Ingrese valores válidos.")

        elif opcion == "2":
            try:
                id_producto = int(input("Ingrese ID del producto a eliminar: "))
                inventario.eliminar_producto(id_producto)
            except ValueError:
                print("❌ Error: El ID debe ser numérico.")

        elif opcion == "3":
            try:
                id_producto = int(input("Ingrese ID del producto a actualizar: "))
                cantidad = input("Nueva cantidad (Enter para omitir): ")
                precio = input("Nuevo precio (Enter para omitir): ")

                cantidad = int(cantidad) if cantidad else None
                precio = float(precio) if precio else None

                inventario.actualizar_producto(id_producto, cantidad, precio)
            except ValueError:
                print("❌ Error: Ingrese valores válidos.")

        elif opcion == "4":
            nombre = input("Ingrese nombre o parte del nombre a buscar: ")
            inventario.buscar_producto(nombre)

        elif opcion == "5":
            inventario.mostrar_todos()

        elif opcion == "6":
            print("👋 Saliendo del sistema de inventarios...")
            break
        else:
            print("❌ Opción no válida. Intente nuevamente.")


# -----------------------
# Ejecución principal
# -----------------------
if __name__ == "__main__":
    menu()
