"""
Support for C++ files to generate PlantUML files.
"""
import subprocess
import os
from overrides import override
from api import CddeAPI
from puml_generator import PumlGenerator


class CppPumlGenerator(PumlGenerator):
    """
    PlantUML generator for C++ files.
    """
    @override
    def generate_plantuml(self, file_path: str) -> str:
        """
        Generate the PlantUML file.
        """
        if not os.path.isfile(file_path):
            return "Error: The specified file does not exist."

        directory = os.path.dirname(file_path)
        name = os.path.basename(file_path)
        return _hpp2plantuml(directory, name, file_path)


def _hpp2plantuml(directory: str, name: str, file_path: str) -> str:
    """
    run hpp2plantuml
    """
    subprocess.run(['hpp2plantuml', '-i', file_path, '-o', directory +
                   '/' + name.replace('.c++', '.plantuml')], check=True)
    file_path = directory + '/' + name.replace('.c++', '.plantuml')
    return file_path


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module of the API.
    """
    api.register_puml_generator('.cpp', CppPumlGenerator)
