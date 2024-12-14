"""
Support for Python files to generate PlantUML files.
"""
import subprocess
import os
from overrides import override
from api import CddeAPI
from puml_generator import PumlGenerator


class PyPumlGenerator(PumlGenerator):
    """
    PlantUML generator for Python files.
    """
    @override
    def generate_plantuml(self, directory: str) -> str:
        """
        Generate the PlantUML file.
        """
        if not os.path.isdir(directory):
            return "Error: The specified file does not exist."
        if directory[-1] != '/':
            directory += '/'
        return _pyreverse(directory)


def _py_files(directory: str) -> list:
    """
    Get the python files in the directory and return them as a string
    """
    files = []
    for root, _, files_in_dir in os.walk(directory):
        for file in files_in_dir:
            if file.endswith('.py'):
                files.append(os.path.join(root, file))
    return files


def _pyreverse(directory: str) -> str:
    """
    run pyreverse
    """
    files = _py_files(directory)
    subprocess.run(['pyreverse', '-o', 'plantuml', '-p',
                   'UML', '-d', directory] + files, check=True)

    if os.path.isfile(directory + 'packages_UML.plantuml'):
        packages = directory + 'packages_UML.plantuml'
        subprocess.run(['rm', '-rf', packages], check=True)

    file_path = directory + "classes_" + 'UML.plantuml'
    return file_path


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module of the API
    """
    api.register_puml_generator('.py', PyPumlGenerator)
