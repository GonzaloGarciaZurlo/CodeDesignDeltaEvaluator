#ifndef PAYPAL_PROCESSOR_H
#define PAYPAL_PROCESSOR_H

#include "payment_processor.hpp"
#include <iostream>

// Clase PayPalProcessor implementa PaymentProcessor
class PayPalProcessor : public PaymentProcessor {
public:
    void processPayment(float amount) const override {
        std::cout << "Processing PayPal payment of " << amount << " USD." << std::endl;
    }
};

#endif // PAYPAL_PROCESSOR_H
