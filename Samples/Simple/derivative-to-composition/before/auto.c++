#include "auto.hpp"
#include <iostream>

Auto::Auto(const std::string& marca, const std::string& modelo, int puertas)
    : Vehiculo(marca, modelo), puertas(puertas) {}

void Auto::mostrarInfo() const {
    std::cout << "Auto: " << marca << " " << modelo 
              << " con " << puertas << " puertas." << std::endl;
}
