"""
This module handles the main execution flow of the application.
"""
from parser_puml import regex_uml, pyreverse_util, composable_observer, printer
from relationship_db import create_db_neo4j
from db_storer import queries


class Main:
    """
    Main class that coordinates the execution of the program.
    """
    @staticmethod
    def ejecutar():
        """
        Executes the main logic of the program.
        """

        console = printer.Printer()
        db_neo4j = create_db_neo4j.Neo4j()
        observer = composable_observer.Composable([console, db_neo4j])
        parser = regex_uml.Regex(observer)

        db_neo4j.delete_all()  # Eliminar la base de datos

        archivo_cpp = "Samples/Simple/derivative to composition/before.c++"
        #archivo_go = "Samples/Simple/double derivative/before.go"
        #archivo_py = "Samples/SOLID+LoD/I/ISP_P.py"

        archivo_plantuml = pyreverse_util.generate_plantuml(
            archivo_cpp)  # Generar el archivo .plantuml
        parser.parse(archivo_plantuml)


        clasePy = "ISP_P.Trabajador"
        claseGo = "Vehiculo"
        claseCpp = "Auto"
        # Consultar el acoplamiento de una clase
        acoplamiento = queries.Neo4jCoupling().get_class_coupling(claseCpp)
        print(acoplamiento)

        # Eliminar el archivo .plantuml
        pyreverse_util.delete_plantuml(archivo_plantuml)


# Ejecución del ejemplo
if __name__ == "__main__":
    Main.ejecutar()
