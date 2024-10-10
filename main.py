"""
This module handles the main execution flow of the application.
"""
from parser import regex_uml, pyreverse_util
from graph_db import create_db_neo4j
from metricsCollecter import queries


class Main:
    """
    Main class that coordinates the execution of the program.
    """
    @staticmethod
    def ejecutar():
        """
        Executes the main logic of the program.
        """
        observer = create_db_neo4j.Neoj4()
        parser = regex_uml.Regex(observer)

        observer.delete_all()  # Eliminar la base de datos

        #archivo_go = "Samples/Simple/double derivative/before.go"
        archivo_py = "Samples/SOLID+LoD/I/ISP_P.py"

        archivo_plantuml = pyreverse_util.generate_plantuml_python(
            archivo_py)  # Generar el archivo .plantuml
        parser.parse(archivo_plantuml)

        #Consultar el acoplamiento de una clase
        acoplamiento = queries.Neo4jCoupling().get_class_coupling('ISP_P.Trabajador')
        print(acoplamiento)

        # Eliminar el archivo .plantuml
        pyreverse_util.delete_plantuml(archivo_plantuml)


# Ejecución del ejemplo
if __name__ == "__main__":
    Main.ejecutar()
