# Programa: cálculo del área de un círculo
# Autor: [Tu nombre aquí]
# Descripción: Este programa solicita al usuario el radio de un círculo, calcula su área
# utilizando la fórmula A = π * r^2 y muestra el resultado. Se usan diferentes tipos de datos
# y buenas prácticas de codificación en Python.

import math  # Importa la biblioteca matemática para usar pi

# Función que calcula el área de un círculo dado su radio
def calcular_area_circulo(radio: float) -> float:
    """Calcula el área del círculo usando la fórmula A = π * r^2"""
    return math.pi * (radio ** 2)

# Solicita al usuario que ingrese el radio del círculo
radio_usuario = input("Ingrese el radio del círculo: ")
radio_convertido = float(radio_usuario)  # Convierte la entrada a tipo float

# Validación booleana: el radio debe ser mayor que cero
es_valido = radio_convertido > 0

if es_valido:
    area = calcular_area_circulo(radio_convertido)  # Llama a la función para obtener el área
    print("El área del círculo es:", area)  # Muestra el resultado al usuario
else:
    print("El valor ingresado no es válido. El radio debe ser mayor que cero.")