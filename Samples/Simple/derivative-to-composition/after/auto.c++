#include "auto.hpp"
#include <iostream>

Auto::Auto(const std::string& marca, const std::string& modelo, int puertas)
    : vehiculo(marca, modelo), puertas(puertas) {}

void Auto::arrancar() const {
    vehiculo.arrancar();
}

void Auto::detener() const {
    vehiculo.detener();
}

void Auto::mostrarInfo() const {
    std::cout << "Auto: " << vehiculo.getMarca() << " " << vehiculo.getModelo() 
              << " con " << puertas << " puertas." << std::endl;
}
