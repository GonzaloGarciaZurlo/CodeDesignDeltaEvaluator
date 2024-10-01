#ifndef VEHICULO_AUTO_H
#define VEHICULO_AUTO_H

#include <iostream>
#include <string>

class Vehiculo {
protected:
    std::string marca;
    std::string modelo;

public:
    Vehiculo(const std::string& marca, const std::string& modelo) 
        : marca(marca), modelo(modelo) {}

    void arrancar() const {
        std::cout << "El " << marca << " " << modelo << " está arrancando." << std::endl;
    }

    void detener() const {
        std::cout << "El " << marca << " " << modelo << " se ha detenido." << std::endl;
    }
};

class Auto : public Vehiculo {
private:
    int puertas;

public:
    Auto(const std::string& marca, const std::string& modelo, int puertas) 
        : Vehiculo(marca, modelo), puertas(puertas) {}

    void mostrarInfo() const {
        std::cout << "Auto: " << marca << " " << modelo 
                  << " con " << puertas << " puertas." << std::endl;
    }
};

#endif
