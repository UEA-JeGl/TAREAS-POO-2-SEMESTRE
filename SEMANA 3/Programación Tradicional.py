# Programa en estilo tradicional para calcular el promedio semanal del clima

def ingresar_temperaturas():
    """Función para ingresar temperaturas diarias durante una semana"""
    temperaturas = []
    print("Ingrese la temperatura de cada día de la semana:")
    for i in range(7):
        temp = float(input(f"Día {i + 1}: "))
        temperaturas.append(temp)
    return temperaturas

def calcular_promedio(temperaturas):
    """Calcula el promedio de una lista de temperaturas"""
    if len(temperaturas) == 0:
        return 0
    return sum(temperaturas) / len(temperaturas)

def mostrar_resultado(promedio):
    """Muestra el resultado del promedio"""
    print(f"\nEl promedio semanal de temperatura es: {promedio:.2f}°C")

# Ejecución del programa
datos = ingresar_temperaturas()
prom = calcular_promedio(datos)
mostrar_resultado(prom)