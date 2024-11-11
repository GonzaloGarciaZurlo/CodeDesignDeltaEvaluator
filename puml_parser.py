"""
Module that contains the PUML_Parser abstract class
"""
from abc import ABC, abstractmethod
from puml_observer import Observer


class PumlParser(ABC):
    """
    Abstract class that represents a PUML parser.
    """

    def __init__(self, observer: Observer, label: str) -> None:
        self.observer = observer
        self.label = label

    @abstractmethod
    def parse_uml(self, file: str) -> None:
        """
        Parse the PUML file, and set label (after or before).
        """
