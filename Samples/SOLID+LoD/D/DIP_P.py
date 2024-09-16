class Motor:
    def encender(self):
        print("El motor está encendido.")

    def apagar(self):
        print("El motor está apagado.")

class Controlador:
    def __init__(self, motor):
        self.motor = motor

    def activar_motor(self):
        self.motor.encender()

    def desactivar_motor(self):
        self.motor.apagar()

# Uso
motor = Motor()
controlador = Controlador(motor)
controlador.activar_motor()
