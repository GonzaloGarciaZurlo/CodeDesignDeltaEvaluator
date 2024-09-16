class Empleado:
    def __init__(self, nombre, salario):
        self.nombre = nombre
        self.salario = salario

    def calcular_salario_anual(self):
        return self.salario * 12

    def generar_reporte_empleado(self):
        return f"Empleado: {self.nombre}, Salario Anual: {self.calcular_salario_anual()}"


# Uso de la clase
empleado = Empleado("Juan", 3000)
print(empleado.generar_reporte_empleado())
