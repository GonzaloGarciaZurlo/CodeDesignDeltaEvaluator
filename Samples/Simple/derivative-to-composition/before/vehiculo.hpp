#ifndef VEHICULO_H
#define VEHICULO_H

#include <string>

class Vehiculo {
protected:
    std::string marca;
    std::string modelo;

public:
    Vehiculo(const std::string& marca, const std::string& modelo);
    void arrancar() const;
    void detener() const;
};

#endif