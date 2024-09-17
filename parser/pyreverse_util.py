import subprocess
import os

def generate_plantuml_python(file_path: str) -> str:

    if not os.path.isfile(file_path):
        return "Error: The specified file does not exist."

    # Obtener el directorio del archivo .py
    directory = os.path.dirname(file_path)
    # Obtener el nombre del archivo .py
    name = os.path.basename(file_path)

    try:
        subprocess.run(['pyreverse', '-o', 'plantuml', '-p', name.replace('.py', ''), '-d', directory, file_path], check=True)

        return directory + "/classes_" + name.replace('.py', '.plantuml') # Devolver la ruta del archivo .plantuml

    except subprocess.CalledProcessError:

        return "Error: Failed to generate .plantuml file."


def delete_plantuml(file_path: str) -> None:

    if not os.path.isfile(file_path):
        return "Error: The specified file does not exist."

    try:
        subprocess.run(['rm', '-rf', file_path], check=True)

    except subprocess.CalledProcessError:

        return "Error: Failed to delete .plantuml file."
