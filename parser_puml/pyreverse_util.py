"""
module that generates the plantuml file from a python, go or c++ file,
and deletes the plantuml file
"""
import subprocess
import os


def _pyreverse(directory: str, name: str, file_path: str) -> str:
    """
    run pyreverse
    """
    subprocess.run(['pyreverse', '-o', 'plantuml', '-p',
                    name.replace('.py', ''), '-d', directory, file_path], check=True)

    file_path = directory + "/classes_" + name.replace('.py', '.plantuml')
    return file_path


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


def _hpp2plantuml(directory: str, name: str, file_path: str) -> str:
    """
    run hpp2plantuml
    """
    subprocess.run(['hpp2plantuml', '-i', file_path, '-o', directory +
                   '/' + name.replace('.c++', '.plantuml')], check=True)
    file_path = directory + '/' + name.replace('.c++', '.plantuml')
    return file_path


def _deaspacher_plantuml(extension: str, directory: str, name: str, file_path: str) -> str:
    """
    Deaspacher for the plantuml generation
    """
    try:
        match extension:
            case '.py':
                return _pyreverse(directory, name, file_path)
            case '.go':
                return _goplantuml(directory, name, file_path)
            case '.c++':
                return _hpp2plantuml(directory, name, file_path)
            case _:
                return "Error: The file extension is not supported."
    except subprocess.CalledProcessError:
        return "Error: Failed to generate .plantuml file."


def generate_plantuml(file_path: str) -> str:
    """
    Generate the PlantUML file.
    """

    if not os.path.isfile(file_path):
        return "Error: The specified file does not exist."

    directory = os.path.dirname(file_path)
    name = os.path.basename(file_path)
    extension = os.path.splitext(name)[1]

    return _deaspacher_plantuml(extension, directory, name, file_path)


def delete_plantuml(uml_path: str) -> None:
    """
    delete the plantuml file
    """
    try:
        subprocess.run(['rm', '-rf', uml_path], check=True)

    except subprocess.CalledProcessError:
        print("Error: Failed to delete .plantuml file.")
