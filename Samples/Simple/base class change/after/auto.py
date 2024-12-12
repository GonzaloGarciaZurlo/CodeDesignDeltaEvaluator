from motor import Motor


class Auto(Motor):
    def __init__(self, tipo_motor, puertas):
        super().__init__(tipo_motor)
        self.puertas = puertas

    def mostrar_info(self):
        print(f"Auto con motor {self.tipo_motor} y {self.puertas} puertas.")
