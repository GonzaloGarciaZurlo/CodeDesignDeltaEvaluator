from abc import ABC, abstractmethod

class Motor(ABC):
    @abstractmethod
    def encender(self):
        pass

    @abstractmethod
    def apagar(self):
        pass

class MotorCombustion(Motor):
    def encender(self):
        print("El motor de combustión está encendido.")

    def apagar(self):
        print("El motor de combustión está apagado.")

class MotorElectrico(Motor):
    def encender(self):
        print("El motor eléctrico está encendido.")

    def apagar(self):
        print("El motor eléctrico está apagado.")

class Controlador:
    def __init__(self, motor: Motor):
        self.motor = motor

    def activar_motor(self):
        self.motor.encender()

    def desactivar_motor(self):
        self.motor.apagar()

# Uso
motor_combustion = MotorCombustion()
controlador1 = Controlador(motor_combustion)
controlador1.activar_motor()  # Salida: El motor de combustión está encendido.

motor_electrico = MotorElectrico()
controlador2 = Controlador(motor_electrico)
controlador2.activar_motor()  # Salida: El motor eléctrico está encendido.
