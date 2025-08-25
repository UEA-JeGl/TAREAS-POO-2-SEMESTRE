# -------------------------------------------------------
# Sistema de Gestión de Inventarios
# Autor: [Tu Nombre]
# Descripción:
# Este programa implementa un sistema de gestión de inventarios
# para una tienda, utilizando Programación Orientada a Objetos.
# Se manejan productos mediante una lista y se permite
# añadir, actualizar, eliminar, buscar y listar productos.
# -------------------------------------------------------

# -----------------------
# Clase Producto
# -----------------------
class Producto:
    def __init__(self, id_producto: int, nombre: str, cantidad: int, precio: float):
        """
        Constructor de la clase Producto.
        :param id_producto: Identificador único del producto.
        :param nombre: Nombre del producto.
        :param cantidad: Cantidad disponible en inventario.
        :param precio: Precio unitario del producto.
        """
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Métodos Getters y Setters
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


# -----------------------
# Clase Inventario
# -----------------------
class Inventario:
    def __init__(self):
        """
        Constructor que inicializa una lista vacía de productos.
        """
        self.productos = []

    def agregar_producto(self, producto: Producto):
        """
        Agregar un nuevo producto si el ID no existe.
        """
        for p in self.productos:
            if p.get_id() == producto.get_id():
                print("❌ Error: Ya existe un producto con ese ID.")
                return
        self.productos.append(producto)
        print("✅ Producto agregado con éxito.")

    def eliminar_producto(self, id_producto: int):
        """
        Eliminar producto por su ID.
        """
        for p in self.productos:
            if p.get_id() == id_producto:
                self.productos.remove(p)
                print("✅ Producto eliminado.")
                return
        print("❌ Error: No se encontró un producto con ese ID.")

    def actualizar_producto(self, id_producto: int, nueva_cantidad=None, nuevo_precio=None):
        """
        Actualizar cantidad o precio de un producto.
        """
        for p in self.productos:
            if p.get_id() == id_producto:
                if nueva_cantidad is not None:
                    p.set_cantidad(nueva_cantidad)
                if nuevo_precio is not None:
                    p.set_precio(nuevo_precio)
                print("✅ Producto actualizado.")
                return
        print("❌ Error: No se encontró un producto con ese ID.")

    def buscar_producto(self, nombre: str):
        """
        Buscar productos que contengan el nombre indicado.
        """
        resultados = [p for p in self.productos if nombre.lower() in p.get_nombre().lower()]
        if resultados:
            print("🔍 Resultados de la búsqueda:")
            for p in resultados:
                print(p)
        else:
            print("❌ No se encontraron productos con ese nombre.")

    def mostrar_todos(self):
        """
        Mostrar todos los productos en el inventario.
        """
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
