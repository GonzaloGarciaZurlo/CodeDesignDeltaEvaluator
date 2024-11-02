package main

// Vehiculo es la estructura principal
type Vehiculo struct {
    marca string
}

// Auto es una subestructura de Vehiculo
type Auto struct {
    Vehiculo
    puertas int
}

// Moto es otra subestructura de Vehiculo
type Moto struct {
    Vehiculo
    cilindrada int
}