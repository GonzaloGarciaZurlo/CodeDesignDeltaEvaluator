#ifndef CREDIT_CARD_PROCESSOR_H
#define CREDIT_CARD_PROCESSOR_H

#include "payment_processor.hpp"
#include <iostream>

// Clase CreditCardProcessor implementa PaymentProcessor
class CreditCardProcessor : public PaymentProcessor {
public:
    void processPayment(float amount) const override {
        std::cout << "Processing Credit Card payment of " << amount << " USD." << std::endl;
    }
};

#endif // CREDIT_CARD_PROCESSOR_H
