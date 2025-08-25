# Clase que representa a un Usuario del sistema
class Usuario:
    # Método constructor: se ejecuta automáticamente al crear un objeto
    def __init__(self, nombre, correo):
        self.nombre = nombre
        self.correo = correo
        print(f"[INFO] Usuario '{self.nombre}' creado correctamente.")

    # Método para mostrar la información del usuario
    def mostrar_info(self):
        print(f"Nombre: {self.nombre}, Correo: {self.correo}")

    # Método destructor: se ejecuta automáticamente cuando el objeto es eliminado
    def __del__(self):
        print(f"[INFO] El objeto Usuario '{self.nombre}' ha sido eliminado.")


# Clase que representa un sistema con múltiples usuarios
class Sistema:
    def __init__(self):
        self.lista_usuarios = []
        print("[INFO] Sistema iniciado.")

    def agregar_usuario(self, nombre, correo):
        usuario = Usuario(nombre, correo)
        self.lista_usuarios.append(usuario)
        print(f"[INFO] Usuario '{nombre}' agregado al sistema.")

    def mostrar_usuarios(self):
        print("[INFO] Lista de usuarios registrados:")
        for usuario in self.lista_usuarios:
            usuario.mostrar_info()

    def __del__(self):
        print("[INFO] Cerrando el sistema y eliminando usuarios...")

# Bloque principal de ejecución
if __name__ == "__main__":
    # Crear instancia del sistema
    sistema = Sistema()

    # Agregar algunos usuarios
    sistema.agregar_usuario("Ana López", "ana@gmail.com")
    sistema.agregar_usuario("Carlos Ruiz", "carlos@gmail.com")

    # Mostrar todos los usuarios registrados
    sistema.mostrar_usuarios()

    # El destructor del sistema y de cada objeto Usuario se ejecutará al finalizar el programa automáticamente