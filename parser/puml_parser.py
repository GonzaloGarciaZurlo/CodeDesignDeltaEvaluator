from abc import ABC, abstractmethod
import puml_observer


class PUML_Parser(ABC):
    def __init__(self, observer: puml_observer.Observer) -> None:
        self.observer = observer

    @abstractmethod
    def parse(self, file: str, puml_obs: puml_observer.Observer) -> None:
        "Método abstracto que debe implementar cada parser"
        pass
