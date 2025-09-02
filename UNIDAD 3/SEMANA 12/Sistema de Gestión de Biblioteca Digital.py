# ===========================================
# Sistema de Gestión de Biblioteca Digital
# ===========================================

# Clase Libro: representa un libro dentro de la biblioteca
class Libro:
    def __init__(self, titulo, autor, categoria, isbn):
        # Guardamos título y autor en una tupla, ya que no cambian
        self.datos = (titulo, autor)
        self.categoria = categoria
        self.isbn = isbn

    def __str__(self):
        return f"{self.datos[0]} de {self.datos[1]} | Categoría: {self.categoria} | ISBN: {self.isbn}"


# Clase Usuario: representa a un usuario registrado en la biblioteca
class Usuario:
    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista de libros que el usuario tiene prestados

    def __str__(self):
        return f"Usuario: {self.nombre} | ID: {self.id_usuario}"


# Clase Biblioteca: gestiona libros, usuarios y préstamos
class Biblioteca:
    def __init__(self):
        self.libros = {}        # Diccionario {isbn: objeto Libro}
        self.usuarios = {}      # Diccionario {id_usuario: objeto Usuario}
        self.ids_usuarios = set()  # Conjunto para asegurar IDs únicos

    # =====================
    # Métodos para Libros
    # =====================
    def agregar_libro(self, libro):
        if libro.isbn not in self.libros:
            self.libros[libro.isbn] = libro
            print(f"Libro agregado: {libro}")
        else:
            print("Ese libro ya existe en el catálogo.")

    def quitar_libro(self, isbn):
        if isbn in self.libros:
            eliminado = self.libros.pop(isbn)
            print(f"Libro eliminado: {eliminado}")
        else:
            print("No se encontró un libro con ese ISBN.")

    def buscar_libro(self, criterio, valor):
        resultados = []
        for libro in self.libros.values():
            if criterio == "titulo" and valor.lower() in libro.datos[0].lower():
                resultados.append(libro)
            elif criterio == "autor" and valor.lower() in libro.datos[1].lower():
                resultados.append(libro)
            elif criterio == "categoria" and valor.lower() in libro.categoria.lower():
                resultados.append(libro)
        return resultados

    # =====================
    # Métodos para Usuarios
    # =====================
    def registrar_usuario(self, usuario):
        if usuario.id_usuario not in self.ids_usuarios:
            self.usuarios[usuario.id_usuario] = usuario
            self.ids_usuarios.add(usuario.id_usuario)
            print(f"Usuario registrado: {usuario}")
        else:
            print("El ID de usuario ya está en uso.")

    def eliminar_usuario(self, id_usuario):
        if id_usuario in self.usuarios:
            eliminado = self.usuarios.pop(id_usuario)
            self.ids_usuarios.remove(id_usuario)
            print(f"Usuario eliminado: {eliminado}")
        else:
            print("No se encontró ese usuario.")

    # =====================
    # Métodos de Préstamos
    # =====================
    def prestar_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios:
            print("Usuario no registrado.")
            return
        if isbn not in self.libros:
            print("El libro no está disponible en el catálogo.")
            return

        usuario = self.usuarios[id_usuario]
        libro = self.libros.pop(isbn)  # Quitamos el libro del catálogo
        usuario.libros_prestados.append(libro)
        print(f"Préstamo realizado: {usuario.nombre} recibió '{libro.datos[0]}'")

    def devolver_libro(self, id_usuario, isbn):
        if id_usuario not in self.usuarios:
            print("Usuario no registrado.")
            return

        usuario = self.usuarios[id_usuario]
        for libro in usuario.libros_prestados:
            if libro.isbn == isbn:
                usuario.libros_prestados.remove(libro)
                self.libros[isbn] = libro  # Lo regresamos al catálogo
                print(f"Devolución realizada: '{libro.datos[0]}' regresó a la biblioteca")
                return
        print("El usuario no tiene prestado ese libro.")

    def listar_prestamos_usuario(self, id_usuario):
        if id_usuario not in self.usuarios:
            print("Usuario no registrado.")
            return

        usuario = self.usuarios[id_usuario]
        if usuario.libros_prestados:
            print(f"Libros prestados a {usuario.nombre}:")
            for libro in usuario.libros_prestados:
                print(f" - {libro}")
        else:
            print(f"{usuario.nombre} no tiene libros prestados.")


# =====================
# PRUEBAS DEL SISTEMA
# =====================
if __name__ == "__main__":
    # Crear biblioteca
    biblio = Biblioteca()

    # Agregar libros
    libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", "Novela", "111")
    libro2 = Libro("El Principito", "Antoine de Saint-Exupéry", "Fábula", "222")
    libro3 = Libro("Python para Todos", "Raúl González", "Tecnología", "333")

    biblio.agregar_libro(libro1)
    biblio.agregar_libro(libro2)
    biblio.agregar_libro(libro3)

    # Registrar usuarios
    usuario1 = Usuario("María", "U001")
    usuario2 = Usuario("Carlos", "U002")

    biblio.registrar_usuario(usuario1)
    biblio.registrar_usuario(usuario2)

    # Prestar y devolver libros
    biblio.prestar_libro("U001", "111")
    biblio.prestar_libro("U002", "222")
    biblio.listar_prestamos_usuario("U001")

    biblio.devolver_libro("U001", "111")
    biblio.listar_prestamos_usuario("U001")

    # Buscar libros
    print("\nBúsqueda por autor 'Raúl':")
    encontrados = biblio.buscar_libro("autor", "Raúl")
    for libro in encontrados:
        print(libro)


