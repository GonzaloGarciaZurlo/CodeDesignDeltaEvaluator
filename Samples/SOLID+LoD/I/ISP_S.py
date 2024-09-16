from abc import ABC, abstractmethod

class Trabajador(ABC):
    @abstractmethod
    def trabajar(self):
        pass

    @abstractmethod
    def descansar(self):
        pass

class Reportador(ABC):
    @abstractmethod
    def reportar_progreso(self):
        pass

class Ingeniero(Trabajador, Reportador):
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

# Uso
ingeniero = Ingeniero()
ingeniero.trabajar()
ingeniero.reportar_progreso()

obrero = Obrero()
obrero.trabajar()
# Obrero no necesita reportar progreso
