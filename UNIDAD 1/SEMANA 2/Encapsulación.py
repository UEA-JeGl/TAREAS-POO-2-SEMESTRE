class CuentaBancaria:
    def __init__(self, titular, saldo_inicial=0):
        self.__titular = titular
        self.__saldo = saldo_inicial

    def depositar(self, cantidad):
        if cantidad > 0:
            self.__saldo += cantidad
            print(f"Depósito exitoso. Nuevo saldo: ${self.__saldo}")
        else:
            print("Cantidad no válida para depósito.")

    def retirar(self, cantidad):
        if 0 < cantidad <= self.__saldo:
            self.__saldo -= cantidad
            print(f"Retiro exitoso. Saldo restante: ${self.__saldo}")
        else:
            print("Fondos insuficientes o cantidad inválida.")

    def mostrar_saldo(self):
        print(f"Saldo actual de {self.__titular}: ${self.__saldo}")

# Ejemplo de uso
if __name__ == "__main__":
    cuenta = CuentaBancaria("María", 1000)
    cuenta.depositar(250)
    cuenta.retirar(500)
    cuenta.mostrar_saldo()
