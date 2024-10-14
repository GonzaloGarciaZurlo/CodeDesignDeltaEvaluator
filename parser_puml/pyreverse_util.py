"""
module that generates the plantuml file from a python, go or c++ file,
and deletes the plantuml file
"""
import subprocess
import os


def _pyreverse(directory, name, file_path):
    """
    run pyreverse
    """
    subprocess.run(['pyreverse', '-o', 'plantuml', '-p',
                    name.replace('.py', ''), '-d', directory, file_path], check=True)

    return directory + "/classes_" + name.replace('.py', '.plantuml')


def _goplantuml(directory, name, file_path):
    """
    run goplantuml
    """
    subprocess.Popen(["mkdir", "-p", "temp_dir"])
    subprocess.run(['cp', file_path, 'temp_dir'], check=True)
    with open(directory + '/' + name.replace('.go', '.plantuml'), 'w') as output_file:
        subprocess.run(['goplantuml', 'temp_dir'], stdout=output_file, check=True)
    subprocess.run(['rm', '-rf', './temp_dir'], check=True)

    return directory + '/' + name.replace('.go', '.plantuml')


def _hpp2plantuml(directory, name, file_path):
    """
    run hpp2plantuml
    """
    subprocess.run(['hpp2plantuml', '-i', file_path, '-o', directory +
                   '/' + name.replace('.c++', '.plantuml')], check=True)

    return directory + '/' + name.replace('.c++', '.plantuml')


def _scheduler_plantuml(extension, directory, name, file_path):
    try:
        if extension == '.py':
            return _pyreverse(directory, name, file_path)
        elif extension == '.go':
            return _goplantuml(directory, name, file_path)
        elif extension == '.c++':
            return _hpp2plantuml(directory, name, file_path)
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

    return _scheduler_plantuml(extension, directory, name, file_path)


def delete_plantuml(uml_path: str) -> None:
    """
    delete the plantuml file
    """

    if not os.path.isfile(uml_path):
        print("Error: The specified file does not exist.")

    try:
        subprocess.run(['rm', '-rf', uml_path], check=True)

    except subprocess.CalledProcessError:
        print("Error: Failed to delete .plantuml file.")
