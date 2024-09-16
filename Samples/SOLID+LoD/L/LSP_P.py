class Rectangulo:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    def set_ancho(self, ancho):
        self.ancho = ancho

    def set_alto(self, alto):
        self.alto = alto

    def area(self):
        return self.ancho * self.alto

class Cuadrado(Rectangulo):
    def set_ancho(self, ancho):
        self.ancho = ancho
        self.alto = ancho  # En un cuadrado, ancho y alto deben ser iguales

    def set_alto(self, alto):
        self.ancho = alto
        self.alto = alto  # En un cuadrado, ancho y alto deben ser iguales

# Uso
def imprimir_area(rectangulo):
    print(f"Área: {rectangulo.area()}")

rect = Rectangulo(5, 10)
imprimir_area(rect)  # Salida: Área: 50

cuad = Cuadrado(5, 5)
cuad.set_ancho(6)
imprimir_area(cuad)  # Salida: Área: 36 (esperado) pero podría ser confuso o romper la lógica de Rectángulo
