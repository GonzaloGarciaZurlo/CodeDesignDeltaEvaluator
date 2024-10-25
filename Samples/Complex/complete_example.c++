#include <iostream>
#include <vector>
#include <memory>
#include <string>

// Clase abstracta User
class User {
protected:
    std::string username;
    std::string email;
public:
    User(const std::string& uname, const std::string& mail) : username(uname), email(mail) {}
    virtual std::string getRole() const = 0;  // Método abstracto
};

// Clase concreta Admin hereda de User
class Admin : public User {
    int admin_level;
public:
    Admin(const std::string& uname, const std::string& mail, int level) 
        : User(uname, mail), admin_level(level) {}

    std::string getRole() const override {
        return "Admin";
    }
};

// Clase concreta Customer hereda de User
class Customer : public User {
    int customer_id;
public:
    Customer(const std::string& uname, const std::string& mail, int id)
        : User(uname, mail), customer_id(id) {}

    std::string getRole() const override {
        return "Customer";
    }
};

// Interfaz PaymentProcessor (usando clase abstracta pura)
class PaymentProcessor {
public:
    virtual void processPayment(float amount) const = 0;  // Método abstracto
};

// Clase PayPalProcessor implementa PaymentProcessor
class PayPalProcessor : public PaymentProcessor {
public:
    void processPayment(float amount) const override {
        std::cout << "Processing PayPal payment of " << amount << " USD." << std::endl;
    }
};

// Clase CreditCardProcessor implementa PaymentProcessor
class CreditCardProcessor : public PaymentProcessor {
public:
    void processPayment(float amount) const override {
        std::cout << "Processing Credit Card payment of " << amount << " USD." << std::endl;
    }
};

// Clase ShoppingCart tiene una composición con Customer
class ShoppingCart {
    std::shared_ptr<Customer> customer;
    std::vector<std::string> items;

public:
    ShoppingCart(std::shared_ptr<Customer> cust) : customer(cust) {}

    void addItem(const std::string& item) {
        items.push_back(item);
    }

    float getTotal() const {
        return items.size() * 10.0f;  // Por simplicidad, cada artículo cuesta 10 USD
    }
};

// Clase Order tiene una agregación con Customer y PaymentProcessor
class Order {
    std::shared_ptr<Customer> customer;
    std::shared_ptr<PaymentProcessor> payment_processor;
    std::vector<std::string> items;

public:
    Order(std::shared_ptr<Customer> cust, std::shared_ptr<PaymentProcessor> processor)
        : customer(cust), payment_processor(processor) {}

    void addItem(const std::string& item) {
        items.push_back(item);
    }

    void processOrder() {
        std::cout << "Processing order for " << customer->getRole() << " with items:" << std::endl;
        for (const auto& item : items) {
            std::cout << "- " << item << std::endl;
        }
        float total = items.size() * 10.0f;
        payment_processor->processPayment(total);
    }
};

// Función principal
int main() {
    std::shared_ptr<Customer> customer = std::make_shared<Customer>("JohnDoe", "john@example.com", 123);
    std::shared_ptr<PaymentProcessor> paypal = std::make_shared<PayPalProcessor>();

    // Creando el carrito de compras y agregando items
    ShoppingCart cart(customer);
    cart.addItem("Laptop");
    cart.addItem("Mouse");

    // Creando la orden y procesándola
    Order order(customer, paypal);
    order.addItem("Laptop");
    order.addItem("Mouse");
    order.processOrder();

    return 0;
}
