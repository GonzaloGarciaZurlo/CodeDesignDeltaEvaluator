#ifndef VEHICULO_H
#define VEHICULO_H

#include <string>

class Vehiculo {
private:
    std::string marca;
    std::string modelo;

public:
    Vehiculo(const std::string& marca, const std::string& modelo);
    void arrancar() const;
    void detener() const;
    std::string getMarca() const;
    std::string getModelo() const;
};

#endif
