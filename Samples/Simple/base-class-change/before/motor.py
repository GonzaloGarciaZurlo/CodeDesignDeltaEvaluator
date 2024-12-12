class Motor:
    def __init__(self, tipo_motor):
        self.tipo_motor = tipo_motor

    def encender_motor(self):
        print(f"El motor {self.tipo_motor} está encendido.")

    def apagar_motor(self):
        print(f"El motor {self.tipo_motor} está apagado.")