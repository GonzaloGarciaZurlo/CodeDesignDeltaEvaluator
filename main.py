"""
This module handles the main execution flow of the application.
"""
from api import CddeAPI


class Main:
    """
    Main class that coordinates the execution of the program.
    """
    @staticmethod
    def ejecutar():
        """
        Executes the main logic of the program.
        """

    api = CddeAPI()
    api.load_modules_from_directory("addons")

    # get the generators
    cpp_generator = api.generators['.cpp']()
    py_generator = api.generators['.py']()
    go_generator = api.generators['.go']()

    # get observers
    printer = api.observers['printer']()
    db_neo4j = api.observers['neo4j']()
    composable = api.observers['composable']([printer, db_neo4j])

    # get parsers
    regex = api.parsers['regex'](composable)
    parsimonious = api.parsers['parsimonius'](composable)

    # Delete all nodes and relationships in the database
    db_neo4j.delete_all()

    archivo_cpp = "Samples/Simple/derivative to composition/before.c++"
    archivo_go = "Samples/Simple/double derivative/before.go"
    archivo_py = "Samples/SOLID+LoD/I/ISP_P.py"
    complex_example_py = "Samples/Complex/complete_example.py"
    complex_example_cpp = "Samples/Complex/complete_example.c++"

    # Generar el archivo .plantuml
    archivo_plantuml = cpp_generator.generate_plantuml(complex_example_cpp)

    # Parse the plantuml file
    regex.parse_uml(archivo_plantuml)

    clasePy = "ISP_P.Trabajador"
    claseGo = "Dog"
    claseCpp = "Auto"
    clase_complex_cpp = "User"

    # get results observers
    result_printer = api.results_observers['printer']()

    # get result queries
    cypher = api.result_queries['cypher'](result_printer)

    # Consultar el acoplamiento de una clase
    cypher.resolve_query(clase_complex_cpp)

    # Eliminar el archivo .plantuml
    cpp_generator.delete_plantuml(archivo_plantuml)


# Ejecución del ejemplo
if __name__ == "__main__":
    Main.ejecutar()
