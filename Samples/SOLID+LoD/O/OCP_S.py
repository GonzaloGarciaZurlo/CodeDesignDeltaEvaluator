from abc import ABC, abstractmethod

class Empleado(ABC):
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    @abstractmethod
    def calcular_bonificacion(self):
        pass

class EmpleadoTiempoCompleto(Empleado):
    def calcular_bonificacion(self):
        return self.salario * 0.1

class EmpleadoPorContrato(Empleado):
    def calcular_bonificacion(self):
        return self.salario * 0.05

class SistemaBonificaciones:
    def calcular_bonificacion(self, empleado):
        return empleado.calcular_bonificacion()

# Uso del sistema
empleado_tc = EmpleadoTiempoCompleto("Juan", 3000)
empleado_contrato = EmpleadoPorContrato("Pedro", 2000)

sistema = SistemaBonificaciones()

print(sistema.calcular_bonificacion(empleado_tc))        # Salida: 300.0
print(sistema.calcular_bonificacion(empleado_contrato))  # Salida: 100.0
