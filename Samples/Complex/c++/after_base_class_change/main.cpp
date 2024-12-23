#include "customer.hpp"
#include "shopping_cart.hpp"
#include "order.hpp"
#include "paypal_processor.hpp"
#include <memory>
#include <iostream>

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
