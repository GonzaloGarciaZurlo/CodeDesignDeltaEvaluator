#ifndef AUTO_H
#define AUTO_H

#include "vehiculo.hpp"
#include <string>

class Auto {
private:
    Vehiculo vehiculo;  // Composición: el Auto tiene un Vehiculo
    int puertas;

public:
    Auto(const std::string& marca, const std::string& modelo, int puertas);
    void arrancar() const;
    void detener() const;
    void mostrarInfo() const;
};

#endif
