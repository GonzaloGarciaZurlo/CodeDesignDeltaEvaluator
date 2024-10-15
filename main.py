"""
This module handles the main execution flow of the application.
"""
from parser_puml import regex_uml, pyreverse_util, composable_observer, printer, parser_factory, observer_factory
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

        # Creacion de obsvers 
        console = printer.Printer()
        db_neo4j = create_db_neo4j.Neo4j()
        obs1 = observer_factory.ObserverFactory.create_observer(console)
        obs2 = observer_factory.ObserverFactory.create_observer(db_neo4j)
        composable = composable_observer.Composable([obs1, obs2])
        observer = observer_factory.ObserverFactory.create_observer(composable)

        # Creacion de parser
        regex = regex_uml.Regex(observer)   # parser con regex
        parser = parser_factory.ParserFactory.create_parser(regex)

        obs2.delete_all()  # Eliminar la base de datos

        # archivo_cpp = "Samples/Simple/derivative to composition/before.c++"
        # archivo_go = "Samples/Simple/double derivative/before.go"
        archivo_py = "Samples/SOLID+LoD/I/ISP_P.py"

        # Generar el archivo .plantuml
        archivo_plantuml = pyreverse_util.generate_plantuml(archivo_py)
        parser.parse_uml(archivo_plantuml)

        clasePy = "ISP_P.Trabajador"
        # claseGo = "Vehiculo"
        # claseCpp = "Auto"

        # Consultar el acoplamiento de una clase
        acoplamiento = queries.Neo4jCoupling().get_class_coupling(clasePy)
        print(acoplamiento)

        # Eliminar el archivo .plantuml
        pyreverse_util.delete_plantuml(archivo_plantuml)


# Ejecución del ejemplo
if __name__ == "__main__":
    Main.ejecutar()
