class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def arrancar(self):
        print(f"El {self.marca} {self.modelo} está arrancando.")

    def detener(self):
        print(f"El {self.marca} {self.modelo} se ha detenido.")

