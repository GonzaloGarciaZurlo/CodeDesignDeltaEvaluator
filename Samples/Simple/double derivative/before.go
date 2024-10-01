package main

import (
	"fmt"
)

// Clase base
type Animal struct {
	Name string
}

// Método de la clase base
func (a *Animal) Speak() string {
	return "El animal hace un sonido."
}

// Clase derivada (subclase)
type Dog struct {
	Animal // Composición: Dog "hereda" de Animal
}

// Método de la subclase
func (d *Dog) Speak() string {
	return "¡Guau! ¡Soy " + d.Name + "!"
}

func main() {
	// Crear una instancia de la clase base
	animal := Animal{Name: "General"}
	fmt.Println(animal.Name + ": " + animal.Speak())

	// Crear una instancia de la subclase
	dog := Dog{Animal: Animal{Name: "Rex"}}
	fmt.Println(dog.Name + ": " + dog.Speak())
}
