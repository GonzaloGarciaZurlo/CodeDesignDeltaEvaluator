from abc import ABC, abstractmethod

# Interfaz
class PaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

# Clase abstracta
class User(ABC):
    def __init__(self, username, email):
        self.username = username
        self.email = email

    @abstractmethod
    def get_role(self):
        pass

# Clase concreta que hereda de la clase abstracta User
class Customer(User):
    def __init__(self, username, email, customer_id):
        super().__init__(username, email)
        self.customer_id = customer_id

    def get_role(self):
        return "Customer"

# Clase concreta que hereda de la clase abstracta User
class Admin(User):
    def __init__(self, username, email, admin_level):
        super().__init__(username, email)
        self.admin_level = admin_level

    def get_role(self):
        return "Admin"

# Clase concreta que implementa la interfaz PaymentProcessor
class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing PayPal payment of {amount}...")

# Clase concreta que implementa la interfaz PaymentProcessor
class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount):
        print(f"Processing credit card payment of {amount}...")

# Composición
class ShoppingCart:
    def __init__(self, customer):
        self.customer = customer
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_total(self):
        return sum(item['price'] for item in self.items)

# Agregación
class Order:
    def __init__(self, customer, payment_processor):
        self.customer = customer  # Esto es una agregación
        self.payment_processor = payment_processor  # Esto también es una agregación
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def process_order(self):
        total = sum(item['price'] for item in self.items)
        print(f"Processing order for {self.customer.username}, total: {total}")
        self.payment_processor.process_payment(total)