"""
This module handles the main execution flow of the application.
"""
from parser_puml import pyreverse_util, parser_factory, observer_factory
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

    # crear observers
    console = observer_factory.ObserverFactory.create_observer("printer")
    db_neo4j = observer_factory.ObserverFactory.create_observer("neo4j")
    composable = observer_factory.ObserverFactory.create_observer(
        "composable", [console, db_neo4j])

    # Crear parser
    parser = parser_factory.ParserFactory.create_parser("parsimonius", composable)

    # Eliminar la base de datos
    db_neo4j.delete_all()

    #archivo_cpp = "Samples/Simple/derivative to composition/before.c++"
    #archivo_go = "Samples/Simple/double derivative/before.go"
    archivo_py = "Samples/SOLID+LoD/I/ISP_P.py"

    # Generar el archivo .plantuml
    archivo_plantuml = pyreverse_util.generate_plantuml(archivo_py)
    parser.parse_uml(archivo_plantuml)

    clasePy = "ISP_P.Trabajador"
    #claseGo = "Dog"
    #claseCpp = "Auto"

    # Consultar el acoplamiento de una clase
    acoplamiento = queries.Neo4jCoupling().get_class_coupling(clasePy)
    print(acoplamiento)

    # Eliminar el archivo .plantuml
    pyreverse_util.delete_plantuml(archivo_plantuml)


# Ejecución del ejemplo
if __name__ == "__main__":
    Main.ejecutar()
