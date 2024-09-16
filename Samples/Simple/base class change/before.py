class Vehiculo:
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    def arrancar(self):
        print(f"El {self.marca} {self.modelo} está arrancando.")

    def detener(self):
        print(f"El {self.marca} {self.modelo} se ha detenido.")

class Motor:
    def __init__(self, tipo_motor):
        self.tipo_motor = tipo_motor

    def encender_motor(self):
        print(f"El motor {self.tipo_motor} está encendido.")

    def apagar_motor(self):
        print(f"El motor {self.tipo_motor} está apagado.")

class Auto(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)  # Llama al constructor de Vehiculo
        self.puertas = puertas
    
    def mostrar_info(self):
        print(f"Auto: {self.marca} {self.modelo} con {self.puertas} puertas.")
