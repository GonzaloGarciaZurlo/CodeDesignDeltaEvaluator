import subprocess
import os


def generate_plantuml_python(file_path: str) -> str:

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
        #elif leng == '.go':
        #    subprocess.run(['go-plantuml', 'generate', '-f',  file_path,
        #                   '-o', file_path.replace(leng, '.plantuml')], check=True)
        #    return file_path.replace(leng, '.plantuml')

    except subprocess.CalledProcessError:

        return "Error: Failed to generate .plantuml file."


def delete_plantuml(uml_path: str) -> None:

    if not os.path.isfile(uml_path):
        return "Error: The specified file does not exist."

    try:
        subprocess.run(['rm', '-rf', uml_path], check=True)

    except subprocess.CalledProcessError:

        return "Error: Failed to delete .plantuml file."
