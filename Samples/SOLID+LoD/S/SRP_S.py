class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def calcular_salario_anual(self):
        return self.salario * 12

class ReporteEmpleado:
    def generar_reporte(self, empleado):
        return f"Empleado: {empleado.nombre}, Salario Anual: {empleado.calcular_salario_anual()}"

# Uso de las clases
empleado = Empleado("Juan", 3000)
reporte = ReporteEmpleado()

print(reporte.generar_reporte(empleado))
