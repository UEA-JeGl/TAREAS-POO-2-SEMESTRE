class ClimaSemanal:
    def __init__(self):
        # Lista para almacenar las temperaturas diarias
        self.__temperaturas = []

    def ingresar_datos(self):
        """Método para ingresar temperaturas de los 7 días"""
        print("Ingrese la temperatura de cada día de la semana:")
        for i in range(7):
            temp = float(input(f"Día {i + 1}: "))
            self.__temperaturas.append(temp)

    def calcular_promedio(self):
        """Calcula el promedio de temperaturas"""
        if not self.__temperaturas:
            return 0
        return sum(self.__temperaturas) / len(self.__temperaturas)

    def mostrar_promedio(self):
        """Muestra el resultado del promedio"""
        promedio = self.calcular_promedio()
        print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")

# Ejecución del programa
if __name__ == "__main__":
    clima = ClimaSemanal()
    clima.ingresar_datos()
    clima.mostrar_promedio()
