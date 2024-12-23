#ifndef CUSTOMER_H
#define CUSTOMER_H

#include "user.hpp"
#include "payment_processor.hpp"
// Clase concreta Customer hereda de User
class Customer : public User {
    std::shared_ptr<PaymentProcessor> payment_processor;
    int customer_id;

   public:
    Customer(const std::string& uname, const std::string& mail, int id, std::shared_ptr<PaymentProcessor> processor)
        : User(uname, mail), customer_id(id), payment_processor(processor) {}

    std::string getRole() const override {
        return "Customer";
    }
};

#endif  // CUSTOMER_H
