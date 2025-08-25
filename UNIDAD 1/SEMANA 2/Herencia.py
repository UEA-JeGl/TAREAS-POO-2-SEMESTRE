class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def descripcion(self):
        print(f"Vehículo: {self.marca} {self.modelo}")

class Motocicleta(Vehiculo):
    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self.cilindrada = cilindrada

    def descripcion(self):
        print(f"Motocicleta: {self.marca} {self.modelo}, {self.cilindrada}cc")

# Ejemplo de uso
if __name__ == "__main__":
    moto = Motocicleta("Yamaha", "MT-07", 689)
    moto.descripcion()
