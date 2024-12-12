from vehiculo import Vehiculo


class Auto(Vehiculo):
    def __init__(self, marca, modelo, puertas):
        super().__init__(marca, modelo)  # Llama al constructor de Vehiculo
        self.puertas = puertas

    def mostrar_info(self):
        print(f"Auto: {self.marca} {self.modelo} con {self.puertas} puertas.")
