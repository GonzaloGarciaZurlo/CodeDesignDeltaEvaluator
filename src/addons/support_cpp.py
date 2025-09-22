"""
Support for C++ files to generate PlantUML files.
"""
import subprocess
import os
from pathlib import Path
from overrides import override
from src.cdde.addons_api import CddeAPI
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

    def _cpp_files(self, directory: str) -> list:
        """
        Get the C++ files in the directory and return them as a string.
        """
        files = []
        for root, _, files_in_dir in os.walk(directory):
            files += self._search_cpp_files(files_in_dir, root)
        return files

    def _search_cpp_files(self, files: list[str], root: str) -> list:
        """
        Search for C++ files in the list of files.
        """
        cpp_files = []
        for file in files:
            if file.endswith('.hpp') or file.endswith('.h'):
                cpp_files.append(os.path.join(root, file))
        return cpp_files

    def _hpp2plantuml(self, directory: str) -> str:
        """
        Run hpp2plantuml.
        """
        # Buscar todos los .hpp y .h recursivamente
        files = list(Path(directory).rglob("*.hpp")) + list(Path(directory).rglob("*.h"))

        # Convertir a strings
        files_str = [str(f) for f in files]
        file_path = os.path.join(directory, 'UML.plantuml')
        subprocess.run(['hpp2plantuml', '-o', file_path,
                        '-i'] + files_str, check=True)
        return file_path


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module of the API.
    """
    api.register_puml_generator('cpp', CppPumlGenerator)
