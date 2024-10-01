#ifndef VEHICULO_AUTO_H
#define VEHICULO_AUTO_H

#include <iostream>
#include <string>

class Vehiculo {
private:
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

    std::string getMarca() const { return marca; }
    std::string getModelo() const { return modelo; }
};

class Auto {
private:
    Vehiculo vehiculo;  // Composición: Auto contiene un Vehiculo
    int puertas;

public:
    Auto(const std::string& marca, const std::string& modelo, int puertas) 
        : vehiculo(marca, modelo), puertas(puertas) {}

    void arrancar() const {
        vehiculo.arrancar();
    }

    void detener() const {
        vehiculo.detener();
    }

    void mostrarInfo() const {
        std::cout << "Auto: " << vehiculo.getMarca() << " " << vehiculo.getModelo() 
                  << " con " << puertas << " puertas." << std::endl;
    }
};

#endif
