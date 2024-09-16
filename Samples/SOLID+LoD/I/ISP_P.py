from abc import ABC, abstractmethod

class Trabajador(ABC):
    @abstractmethod
    def trabajar(self):
        pass

    @abstractmethod
    def descansar(self):
        pass

    @abstractmethod
    def reportar_progreso(self):
        pass

class Ingeniero(Trabajador):
    def trabajar(self):
        print("Ingeniero trabajando en el proyecto.")

    def descansar(self):
        print("Ingeniero tomando un descanso.")

    def reportar_progreso(self):
        print("Ingeniero reportando el progreso del proyecto.")

class Obrero(Trabajador):
    def trabajar(self):
        print("Obrero trabajando en la construcción.")

    def descansar(self):
        print("Obrero tomando un descanso.")

    def reportar_progreso(self):
        pass  # Obrero no reporta progreso, pero tiene que implementar el método

# Uso
ingeniero = Ingeniero()
ingeniero.trabajar()
ingeniero.reportar_progreso()

obrero = Obrero()
obrero.trabajar()
obrero.reportar_progreso()  # No hace nada, lo que es un problema
