"""
Support for Go files to generate PlantUML files.
"""
import subprocess
import os
from overrides import override
from api import CddeAPI
from puml_generator import PumlGenerator


class GoPumlGenerator(PumlGenerator):
    """
    PlantUML generator for go files.
    """
    @override
    def generate_plantuml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """
        if not os.path.isdir(directory):
            return "Error: The specified directory does not exist."
        if directory[-1] != '/':
            directory += '/'
        return _goplantuml(directory)


def _goplantuml(directory: str) -> str:
    """
    run goplantuml
    """
    file_path = directory + 'UML.plantuml'
    with open(file_path, 'w', encoding="utf-8") as output_file:
        subprocess.run(['goplantuml', directory],
                       stdout=output_file, check=True)
    return file_path


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module of the API.
    """
    api.register_puml_generator('.go', GoPumlGenerator)
