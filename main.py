from graphDB import create_db_neo4j
from parser import regex_uml, pyreverse_util, printer


class Main:
    @staticmethod
    def ejecutar():
        observer = create_db_neo4j.Neoj4()
        parser = regex_uml.Regex(observer)

        # Parsear un archivo de ejemplo
        archivo_plantuml = pyreverse_util.generate_plantuml_python(
            'Samples/SOLID+LoD/I/ISP_P.py')  # Generar el archivo .plantuml
        parser.parse(archivo_plantuml)
        # Eliminar el archivo .plantuml
        pyreverse_util.delete_plantuml(archivo_plantuml)


# Ejecución del ejemplo
if __name__ == "__main__":
    Main.ejecutar()
