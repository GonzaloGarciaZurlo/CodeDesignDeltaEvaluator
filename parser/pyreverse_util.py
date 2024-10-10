"""
module that generates the plantuml file from a python, go or c++ file,
and deletes the plantuml file
"""
import subprocess
import os


def generate_plantuml_python(file_path: str) -> str:
    """
    generate the plantuml file
    """

    if not os.path.isfile(file_path):
        return "Error: The specified file does not exist."

    # Obtener el directorio del archivo .py
    directory = os.path.dirname(file_path)
    # Obtener el nombre del archivo .py
    name = os.path.basename(file_path)
    leng = name[-3:]

    try:
        if leng == '.py':
            subprocess.run(['pyreverse', '-o', 'plantuml', '-p',
                           name.replace('.py', ''), '-d', directory, file_path], check=True)

            # Devolver la ruta del archivo .plantuml
            return directory + "/classes_" + name.replace(leng, '.plantuml')
        # elif leng == '.go':
        #    subprocess.Popen(["mkdir", "-p", "temp_dir"])
        #    subprocess.run(['cp', file_path, 'temp_dir'])
        #    subprocess.run('goplantuml', './temp_dir', '>', directory +
        #  '/' + name.replace('.go', '.plantuml'))
        #    subprocess.run(['rm', '-rf', 'temp_dir'])

            # Devolver la ruta del archivo .plantuml
        #    return directory + name.replace(leng, '.plantuml')
        return "Error: The file extension is not supported."
    except subprocess.CalledProcessError:

        return "Error: Failed to generate .plantuml file."


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
