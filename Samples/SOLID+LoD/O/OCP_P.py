class EmpleadoTiempoCompleto:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def calcular_bonificacion(self):
        return self.salario * 0.1

class SistemaBonificaciones:
    def calcular_bonificacion(self, empleado):
        if isinstance(empleado, EmpleadoTiempoCompleto):
            return empleado.calcular_bonificacion()
        else:
            raise NotImplementedError("Este tipo de empleado no está soportado.")

# Uso del sistema
empleado = EmpleadoTiempoCompleto("Juan", 3000)
sistema = SistemaBonificaciones()
print(sistema.calcular_bonificacion(empleado))
