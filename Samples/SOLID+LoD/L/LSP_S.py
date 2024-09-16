from abc import ABC, abstractmethod

class Figura(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangulo(Figura):
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto

    def set_ancho(self, ancho):
        self.ancho = ancho

    def set_alto(self, alto):
        self.alto = alto

    def area(self):
        return self.ancho * self.alto

class Cuadrado(Figura):
    def __init__(self, lado):
        self.lado = lado

    def set_lado(self, lado):
        self.lado = lado

    def area(self):
        return self.lado * self.lado

# Uso
def imprimir_area(figura):
    print(f"Área: {figura.area()}")

rect = Rectangulo(5, 10)
imprimir_area(rect)  # Salida: Área: 50

cuad = Cuadrado(6)
imprimir_area(cuad)  # Salida: Área: 36
