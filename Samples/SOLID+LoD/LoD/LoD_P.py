class CuentaBancaria:
    def __init__(self, saldo):
        self.saldo = saldo

class Cliente:
    def __init__(self, nombre, cuenta_bancaria):
        self.nombre = nombre
        self.cuenta_bancaria = cuenta_bancaria

class Banco:
    def __init__(self, cliente):
        self.cliente = cliente

    def obtener_saldo_cliente(self):
        return self.cliente.cuenta_bancaria.saldo  # Violación de LoD, Banco conoce demasiado sobre Cliente

# Uso
cuenta = CuentaBancaria(1000)
cliente = Cliente("Juan", cuenta)
banco = Banco(cliente)

print(banco.obtener_saldo_cliente())  # Salida: 1000
