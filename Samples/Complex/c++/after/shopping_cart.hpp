#ifndef SHOPPING_CART_H
#define SHOPPING_CART_H

#include "customer.hpp"
#include <vector>
#include <string>
#include <memory>

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

#endif
