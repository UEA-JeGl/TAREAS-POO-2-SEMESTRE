# product.py
class Producto:
    def __init__(self, id_: str, nombre: str, cantidad: int, precio: float):
        self.id = str(id_)
        self.nombre = nombre
        self.cantidad = int(cantidad)
        self.precio = float(precio)

    # Getters y setters (si se requiere lógica adicional pueden agregarse)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "cantidad": self.cantidad,
            "precio": self.precio
        }

    @staticmethod
    def from_dict(d):
        return Producto(d["id"], d["nombre"], d["cantidad"], d["precio"])

    def __str__(self):
        return f"{self.id} - {self.nombre}: {self.cantidad} unidades @ {self.precio:.2f}"