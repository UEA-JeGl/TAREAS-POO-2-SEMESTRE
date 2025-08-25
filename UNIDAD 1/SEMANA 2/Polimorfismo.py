class Animal:
    def hacer_sonido(self):
        print("Este animal hace un sonido.")

class Perro(Animal):
    def hacer_sonido(self):
        print("El perro dice: ¡Guau!")

class Gato(Animal):
    def hacer_sonido(self):
        print("El gato dice: ¡Miau!")

# Función que demuestra polimorfismo
def reproducir_sonido(animal):
    animal.hacer_sonido()

# Ejemplo de uso
if __name__ == "__main__":
    animales = [Perro(), Gato(), Animal()]
    for a in animales:
        reproducir_sonido(a)