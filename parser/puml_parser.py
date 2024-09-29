from abc import ABC, abstractmethod
from parser.puml_observer import Observer


class PUML_Parser(ABC):
    def __init__(self, observer: Observer) -> None:
        self.observer = observer

    @abstractmethod
    def parse(self, file: str, puml_obs: Observer) -> None:
        "Método abstracto que debe implementar cada parser"
        pass
