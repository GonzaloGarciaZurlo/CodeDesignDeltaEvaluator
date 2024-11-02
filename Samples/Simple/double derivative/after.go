package main

// Vehiculo es la estructura principal y contiene un Auto
type Vehiculo struct {
    marca string
    auto  Auto
}

// Auto es una subestructura de Vehiculo y contiene una Moto
type Auto struct {
    Vehiculo
    puertas int
    
}

// Moto es una subestructura de Auto
type Moto struct {
    Auto
    cilindrada int
}
