# Programa: sistema_empresa.py

# Clase base: Empleado
class Empleado:
    def __init__(self, nombre, edad, salario):
        # Atributos encapsulados
        self.__nombre = nombre
        self.__edad = edad
        self.__salario = salario

    # Métodos de acceso (getters y setters)
    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre

    def get_salario(self):
        return self.__salario

    def set_salario(self, nuevo_salario):
        self.__salario = nuevo_salario

    def mostrar_info(self):
        return f"Empleado: {self.__nombre}, Edad: {self.__edad}, Salario: ${self.__salario}"

    # Método que será sobrescrito por las clases hijas (polimorfismo)
    def trabajar(self):
        return f"{self.__nombre} está trabajando en tareas generales."


# Clase derivada: Gerente
class Gerente(Empleado):
    def __init__(self, nombre, edad, salario, departamento):
        super().__init__(nombre, edad, salario)
        self.departamento = departamento

    # Polimorfismo: sobrescribir el método trabajar
    def trabajar(self):
        return f"{self.get_nombre()} está gestionando el departamento de {self.departamento}."

    def mostrar_info(self):
        return super().mostrar_info() + f", Departamento: {self.departamento}"


# Clase derivada: Desarrollador
class Desarrollador(Empleado):
    def __init__(self, nombre, edad, salario, lenguaje):
        super().__init__(nombre, edad, salario)
        self.lenguaje = lenguaje

    def trabajar(self):
        return f"{self.get_nombre()} está programando en {self.lenguaje}."

    def mostrar_info(self):
        return super().mostrar_info() + f", Lenguaje: {self.lenguaje}"


# Función principal que ejecuta el programa
def main():
    # Crear instancias de las clases
    gerente1 = Gerente("Laura Gómez", 40, 2500, "Finanzas")
    dev1 = Desarrollador("Carlos Ruiz", 28, 1800, "Python")

    # Mostrar información y comportamiento
    print(gerente1.mostrar_info())
    print(gerente1.trabajar())

    print()

    print(dev1.mostrar_info())
    print(dev1.trabajar())

    print()

    # Ejemplo de encapsulación: cambiar nombre y salario
    print("Actualizando salario del desarrollador...\n")
    dev1.set_salario(2000)
    dev1.set_nombre("Carlos R.")
    print(dev1.mostrar_info())


if __name__ == "__main__":
    main()
