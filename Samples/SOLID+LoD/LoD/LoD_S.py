class CuentaBancaria:
    def __init__(self, saldo):
        self.saldo = saldo

    def obtener_saldo(self):
        return self.saldo

class Cliente:
    def __init__(self, nombre, cuenta_bancaria):
        self.nombre = nombre
        self.cuenta_bancaria = cuenta_bancaria

    def obtener_saldo(self):
        return self.cuenta_bancaria.obtener_saldo()

class Banco:
    def __init__(self, cliente):
        self.cliente = cliente

    def obtener_saldo_cliente(self):
        return self.cliente.obtener_saldo()  # Cumple LoD, Banco no accede directamente a CuentaBancaria

# Uso
cuenta = CuentaBancaria(1000)
cliente = Cliente("Juan", cuenta)
banco = Banco(cliente)

print(banco.obtener_saldo_cliente())  # Salida: 1000
