#ifndef ORDER_H
#define ORDER_H

#include "customer.hpp"
#include <memory>
#include <vector>
#include <string>
#include <iostream>

// Clase Order tiene una agregación con Customer y PaymentProcessor
class Order {
    std::shared_ptr<Customer> customer;
    std::vector<std::string> items;

public:
    Order(std::shared_ptr<Customer> cust)
        : customer(cust) {}

    void addItem(const std::string& item) {
        items.push_back(item);
    }

    void processOrder() {
        std::cout << "Processing order for " << customer->getRole() << " with items:" << std::endl;
        for (const auto& item : items) {
            std::cout << "- " << item << std::endl;
        }
        float total = items.size() * 10.0f;
    }
};

#endif // ORDER_H
