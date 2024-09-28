from abc import ABC, abstractmethod


class PUML_Parser(ABC):
    def __init__(self, observer):
        self.observer = observer

    @abstractmethod
    def parse(self, file, puml_obs):
        "Método abstracto que debe implementar cada parser"
        pass
