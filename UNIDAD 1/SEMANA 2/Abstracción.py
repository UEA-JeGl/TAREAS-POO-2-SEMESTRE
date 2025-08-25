from abc import ABC, abstractmethod

class DispositivoElectronico(ABC):
    @abstractmethod
    def encender(self):
        pass

    @abstractmethod
    def apagar(self):
        pass

class Laptop(DispositivoElectronico):
    def encender(self):
        print("La laptop se está encendiendo...")

    def apagar(self):
        print("La laptop se está apagando...")

# Ejemplo de uso
if __name__ == "__main__":
    mi_laptop = Laptop()
    mi_laptop.encender()
    mi_laptop.apagar()