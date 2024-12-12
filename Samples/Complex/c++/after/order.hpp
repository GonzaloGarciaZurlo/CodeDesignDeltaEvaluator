#ifndef ORDER_H
#define ORDER_H

#include "customer.hpp"
#include "discount_manager.hpp"
#include <vector>
#include <string>
#include <memory>
#include <iostream>

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

#endif
