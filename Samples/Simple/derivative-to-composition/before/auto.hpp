#ifndef AUTO_H
#define AUTO_H

#include "vehiculo.hpp"
#include <string>

class Auto : public Vehiculo {
private:
    int puertas;

public:
    Auto(const std::string& marca, const std::string& modelo, int puertas);
    void mostrarInfo() const;
};

#endif
