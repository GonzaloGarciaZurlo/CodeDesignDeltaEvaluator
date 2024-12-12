#ifndef ORDER_H
#define ORDER_H

#include "customer.hpp"
#include "payment_processor.hpp"
#include <memory>
#include <vector>
#include <string>
#include <iostream>

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

#endif // ORDER_H
