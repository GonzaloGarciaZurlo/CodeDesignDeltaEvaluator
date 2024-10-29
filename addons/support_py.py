from overrides import override
from api import CddeAPI
from puml_generator import PumlGenerator
import subprocess
import os


class PyPumlGenerator(PumlGenerator):
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
        return _pyreverse(directory, name, file_path)


def _pyreverse(directory: str, name: str, file_path: str) -> str:
    """
    run pyreverse
    """
    subprocess.run(['pyreverse', '-o', 'plantuml', '-p',
                    name.replace('.py', ''), '-d', directory, file_path], check=True)

    file_path = directory + "/classes_" + name.replace('.py', '.plantuml')
    return file_path


def init_module(api: CddeAPI) -> None:
    api.register_puml_generator('.py', PyPumlGenerator)