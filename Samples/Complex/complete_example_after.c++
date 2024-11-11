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

// Nueva clase DiscountManager para gestionar descuentos
class DiscountManager {
public:
    float calculateDiscount(float total) const {
        if (total > 50.0f) {
            return total * 0.1f; // 10% de descuento si el total es mayor a 50 USD
        }
        return 0.0f;
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

// Clase Order tiene una agregación con Customer y DiscountManager
class Order {
    std::shared_ptr<Customer> customer;
    std::shared_ptr<DiscountManager> discount_manager;
    std::vector<std::string> items;

public:
    Order(std::shared_ptr<Customer> cust, std::shared_ptr<DiscountManager> manager)
        : customer(cust), discount_manager(manager) {}

    void addItem(const std::string& item) {
        items.push_back(item);
    }

    void processOrder() {
        std::cout << "Processing order for " << customer->getRole() << " with items:" << std::endl;
        for (const auto& item : items) {
            std::cout << "- " << item << std::endl;
        }
        float total = items.size() * 10.0f;
        float discount = discount_manager->calculateDiscount(total);
        float final_total = total - discount;
        std::cout << "Total: " << total << " USD" << std::endl;
        std::cout << "Discount: " << discount << " USD" << std::endl;
        std::cout << "Final total after discount: " << final_total << " USD" << std::endl;
    }
};

// Función principal
int main() {
    std::shared_ptr<Customer> customer = std::make_shared<Customer>("JaneDoe", "jane@example.com", 456);
    std::shared_ptr<DiscountManager> discount_manager = std::make_shared<DiscountManager>();

    // Creando el carrito de compras y agregando items
    ShoppingCart cart(customer);
    cart.addItem("Tablet");
    cart.addItem("Headphones");

    // Creando la orden y procesándola
    Order order(customer, discount_manager);
    order.addItem("Tablet");
    order.addItem("Headphones");
    order.processOrder();

    return 0;
}
