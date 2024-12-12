#include "vehiculo.hpp"
#include <iostream>

Vehiculo::Vehiculo(const std::string& marca, const std::string& modelo) 
    : marca(marca), modelo(modelo) {}

void Vehiculo::arrancar() const {
    std::cout << "El " << marca << " " << modelo << " está arrancando." << std::endl;
}

void Vehiculo::detener() const {
    std::cout << "El " << marca << " " << modelo << " se ha detenido." << std::endl;
}

std::string Vehiculo::getMarca() const {
    return marca;
}

std::string Vehiculo::getModelo() const {
    return modelo;
}
