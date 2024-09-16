class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
    
    def arrancar(self):
        print(f"El {self.marca} {self.modelo} está arrancando.")
    
    def detener(self):
        print(f"El {self.marca} {self.modelo} se ha detenido.")

class Auto(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)  # Llama al constructor de la clase base
        self.puertas = puertas
    
    def mostrar_info(self):
        print(f"Auto: {self.marca} {self.modelo} con {self.puertas} puertas.")
