"""
Abstract class for PlantUML generators.
"""
from abc import ABC, abstractmethod
import subprocess


class PumlGenerator(ABC):
    """
    Abstract class for PlantUML generators.
    """

    @abstractmethod
    def generate_plantuml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """

    def delete_plantuml(self, uml_path: str) -> None:
        """
        Delete the plantuml file.
        """
        try:
            subprocess.run(['rm', '-rf', uml_path], check=True)

        except subprocess.CalledProcessError:
            print("Error: Failed to delete .plantuml file.")
