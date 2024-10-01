// vehiculo_derivacion.go
package vehiculo

import "fmt"

// Clase base
type Vehiculo struct {
	Marca  string
	Modelo string
}

// Método para arrancar el vehículo
func (v *Vehiculo) Arrancar() {
	fmt.Printf("El %s %s está arrancando.\n", v.Marca, v.Modelo)
}

// Método para detener el vehículo
func (v *Vehiculo) Detener() {
	fmt.Printf("El %s %s se ha detenido.\n", v.Marca, v.Modelo)
}

// Subclase Auto
type Auto struct {
	Vehiculo
	Puertas int
}

// Método para mostrar información del Auto
func (a *Auto) MostrarInfo() {
	fmt.Printf("Auto: %s %s con %d puertas.\n", a.Marca, a.Modelo, a.Puertas)
}

// Subclase Camion que ahora hereda de Auto
type Camion struct {
	Auto            // Composición: Camion tiene un Auto
	CargaMaxima int // Peso máximo que puede cargar el camión
}

// Método para mostrar información del Camión
func (c *Camion) MostrarInfo() {
	fmt.Printf("Camión: %s %s con carga máxima de %d kg y %d puertas.\n",
		c.Marca, c.Modelo, c.CargaMaxima, c.Puertas)
}
