"""
Support for C++ files to generate PlantUML files.
"""
import subprocess
import os
from overrides import override
from cdde.addons_api import CddeAPI
from src.cdde.puml_generator import PumlGenerator


class CppPumlGenerator(PumlGenerator):
    """
    PlantUML generator for C++ files.
    """
    @override
    def generate_plantuml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """
        self._check_directory(directory)
        return self._hpp2plantuml(directory)

    def _check_directory(self, directory: str) -> None:
        """
        Check if the directory exists.
        """
        if not os.path.isdir(directory):
            raise ValueError("The specified directory does not exist.")

        if directory[-1] != '/':
            directory += '/'

    def _hpp2plantuml(self, directory: str) -> str:
        """
        Run hpp2plantuml.
        """
        file_path = os.path.join(directory, 'UML.plantuml')
        subprocess.run(['hpp2plantuml', '-o', file_path,
                        '-i', directory + '**/*.hpp'], check=True)
        return file_path


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module of the API.
    """
    api.register_puml_generator('.cpp', CppPumlGenerator)
