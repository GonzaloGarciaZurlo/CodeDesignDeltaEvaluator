"""
Support for Python files to generate PlantUML files.
"""
import subprocess
import os
from overrides import override
from src.cdde.api import CddeAPI
from src.cdde.puml_generator import PumlGenerator


class PyPumlGenerator(PumlGenerator):
    """
    PlantUML generator for Python files.
    """
    @override
    def generate_plantuml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """
        self.__is_a_directory(directory)
        directory = self.__ends_with_slash(directory)
        return self._pyreverse(directory)

    def __is_a_directory(self, directory: str) -> None:
        """
        Check if the directory exists.
        """
        if not os.path.isdir(directory):
            raise ValueError("The specified directory does not exist.")

    def __ends_with_slash(self, directory: str) -> str:
        """
        Check if the directory ends with a slash.
        """
        if directory[-1] != '/':
            directory += '/'
        return directory

    def _py_files(self, directory: str) -> list:
        """
        Get the python files in the directory and return them as a string.
        """
        files = []
        for root, _, files_in_dir in os.walk(directory):
            files += self._search_py_files(files_in_dir, root)
        return files

    def _search_py_files(self, files: list[str], root: str) -> list:
        """
        Search for python files in the list of files.
        """
        py_files = []
        for file in files:
            if file.endswith('.py'):
                py_files.append(os.path.join(root, file))
        return py_files

    def _pyreverse(self, directory: str) -> str:
        """
        Run pyreverse
        """
        files = self._py_files(directory)
        subprocess.run(['pyreverse', '-o', 'plantuml', '-p',
                        'UML', '-d', directory] + files, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if os.path.isfile(directory + 'packages_UML.plantuml'):
            packages = directory + 'packages_UML.plantuml'
            subprocess.run(['rm', '-rf', packages], check=True)

        file_path = directory + "classes_" + 'UML.plantuml'
        return file_path


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module of the API.
    """
    api.register_puml_generator('.py', PyPumlGenerator)
