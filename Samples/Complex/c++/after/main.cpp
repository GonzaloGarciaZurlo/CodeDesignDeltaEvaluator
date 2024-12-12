#include "customer.hpp"
#include "discount_manager.hpp"
#include "shopping_cart.hpp"
#include "order.hpp"
#include <memory>

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
