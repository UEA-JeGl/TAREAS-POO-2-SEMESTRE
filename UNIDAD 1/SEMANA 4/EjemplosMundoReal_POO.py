# Clase base Persona
class Persona:
    def __init__(self, nombre, cedula):
        self.nombre = nombre
        self.cedula = cedula

    def mostrar_info(self):
        return f"Nombre: {self.nombre}, Cédula: {self.cedula}"

# Clase Huesped hereda de Persona (Herencia)
class Huesped(Persona):
    def __init__(self, nombre, cedula, telefono):
        super().__init__(nombre, cedula)
        self.telefono = telefono

    def mostrar_info(self):
        return f"{super().mostrar_info()}, Teléfono: {self.telefono}"

# Clase Habitacion con atributos y encapsulación
class Habitacion:
    def __init__(self, numero, tipo, precio):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.disponible = True

    def reservar(self):
        if self.disponible:
            self.disponible = False
            return True
        return False

    def liberar(self):
        self.disponible = True

    def mostrar_info(self):
        estado = "Disponible" if self.disponible else "Ocupada"
        return f"Habitación {self.numero} ({self.tipo}) - ${self.precio} - {estado}"

# Clase Reserva que relaciona huéspedes con habitaciones (Interacción entre objetos)
class Reserva:
    def __init__(self, huesped, habitacion):
        self.huesped = huesped
        self.habitacion = habitacion

    def confirmar(self):
        if self.habitacion.reservar():
            print(f"Reserva confirmada para {self.huesped.nombre} en habitación {self.habitacion.numero}.")
        else:
            print("La habitación ya está ocupada.")

# Uso del sistema (Simulación)
def main():
    print("=== Sistema de Reservas de Hotel ===\n")

    # Crear huéspedes
    huesped1 = Huesped("Luis Pérez", "0912345678", "0998765432")

    # Crear habitaciones
    hab1 = Habitacion(101, "Individual", 35.0)
    hab2 = Habitacion(102, "Doble", 50.0)

    # Mostrar habitaciones disponibles
    print(hab1.mostrar_info())
    print(hab2.mostrar_info())

    # Crear reserva
    reserva1 = Reserva(huesped1, hab1)
    reserva1.confirmar()

    # Estado actual de la habitación después de reservar
    print(hab1.mostrar_info())

    # Intentar reservar la misma habitación nuevamente
    reserva2 = Reserva(huesped1, hab1)
    reserva2.confirmar()

if __name__ == "__main__":
    main()