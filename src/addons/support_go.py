"""
Support for Go files to generate PlantUML files.
"""
import subprocess
import os
from overrides import override
from cdde.addons_api import CddeAPI
from src.cdde.puml_generator import PumlGenerator


class GoPumlGenerator(PumlGenerator):
    """
    PlantUML generator for Go files.
    """
    @override
    def generate_plantuml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """
        self._check_directory(directory)
        return self._goplantuml(directory)

    def _check_directory(self, directory: str) -> None:
        """
        Check if the directory exists.
        """
        if not os.path.isdir(directory):
            raise ValueError("The specified directory does not exist.")

        if directory[-1] != '/':
            directory += '/'

    def _goplantuml(self, directory: str) -> str:
        """
        Run goplantuml
        """
        file_path = directory + 'UML.plantuml'
        with open(file_path, 'w', encoding="utf-8") as output_file:
            subprocess.run(['goplantuml', '-recursive', directory],
                           stdout=output_file, check=True)
        return file_path


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module of the API.
    """
    api.register_puml_generator('.go', GoPumlGenerator)
