#ifndef PAYMENT_PROCESSOR_H
#define PAYMENT_PROCESSOR_H

// Interfaz PaymentProcessor (usando clase abstracta pura)
class PaymentProcessor {
public:
    virtual void processPayment(float amount) const = 0;  // Método abstracto
};

#endif // PAYMENT_PROCESSOR_H
