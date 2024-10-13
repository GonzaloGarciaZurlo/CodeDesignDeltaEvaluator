"""
module that contains the PUML_Parser abstract class
"""
from abc import ABC, abstractmethod
from parser_puml.puml_observer import Observer


class PumlParser(ABC):
    """
    Abstract class that represents a PUML parser.
    """
    def __init__(self, observer: Observer) -> None:
        self.observer = observer

    @abstractmethod
    def parse(self, file: str) -> None:
        "Método abstracto que debe implementar cada parser"
