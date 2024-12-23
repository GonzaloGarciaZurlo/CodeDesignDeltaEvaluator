#ifndef ADMIN_H
#define ADMIN_H

#include "customer.hpp"

// Clase concreta Admin hereda de Customer
class Admin : public Customer {
    int admin_level;
public:
    Admin(const std::string& uname, const std::string& mail, int level) 
        : Customer(uname, mail, 0, nullptr), admin_level(level) {}

    std::string getRole() const override {
        return "Admin";
    }
};

#endif // ADMIN_H
