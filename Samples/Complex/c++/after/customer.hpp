#ifndef CUSTOMER_H
#define CUSTOMER_H

#include "user.hpp"

class Customer : public User {
    int customer_id;
public:
    Customer(const std::string& uname, const std::string& mail, int id)
        : User(uname, mail), customer_id(id) {}

    std::string getRole() const override {
        return "Customer";
    }
};

#endif
