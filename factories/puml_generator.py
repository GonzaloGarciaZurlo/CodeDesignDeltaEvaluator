"""
Abstract class for PlantUML generators.
"""
from abc import ABC, abstractmethod


class PumlGenerator(ABC):
    """
    Abstract class for PlantUML generators.
    """

    @abstractmethod
    def generate_plantuml(self, file_path: str) -> str:
        """
        Generate the PlantUML file.
        """
        pass
