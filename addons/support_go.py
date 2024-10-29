from overrides import override
from api import CddeAPI

from puml_generator import PumlGenerator
import subprocess
import os


class GoPumlGenerator(PumlGenerator):
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
        return _goplantuml(directory, name, file_path)


def _goplantuml(directory: str, name: str, file_path: str) -> str:
    """
    run goplantuml
    """
    subprocess.Popen(["mkdir", "-p", "temp_dir"])
    subprocess.run(['cp', file_path, 'temp_dir'], check=True)
    with open(directory + '/' + name.replace('.go', '.plantuml'),
              'w', encoding="utf-8") as output_file:
        subprocess.run(['goplantuml', 'temp_dir'],
                       stdout=output_file, check=True)
    subprocess.run(['rm', '-rf', './temp_dir'], check=True)

    file_path = directory + '/' + name.replace('.go', '.plantuml')
    return file_path


def init_module(api: CddeAPI) -> None:
    api.register_puml_generator('.go', GoPumlGenerator)
