"""
This module handles the main execution flow of the application.
"""
from api import CddeAPI


class Main:
    """
    Main class that coordinates the execution of the program.
    """
    @staticmethod
    def execute():
        """
        Executes the main logic of the program.
        """

    api = CddeAPI()
    api.load_modules_from_directory("addons")

    # Get the generators
    cpp_generator = api.generators['.cpp']()
    py_generator = api.generators['.py']()
    go_generator = api.generators['.go']()

    # Get observers
    printer = api.observers['printer']()
    db_neo4j = api.observers['neo4j']()
    composable = api.observers['composable']([printer, db_neo4j])

    # Get parsers
    regex = api.parsers['regex'](composable)
    parsimonious = api.parsers['parsimonius'](composable)

    # Delete all nodes and relationships in the database
    db_neo4j.delete_all()

    archivo_cpp = "Samples/Simple/derivative to composition/before.c++"
    archivo_go = "Samples/Simple/double derivative/after.go"
    archivo_py = "Samples/SOLID+LoD/I/ISP_P.py"
    complex_example_py = "Samples/Complex/complete_example.py"
    complex_example_cpp = "Samples/Complex/complete_example.c++"

    # Generate the plantuml file
    archivo_plantuml = cpp_generator.generate_plantuml(complex_example_cpp)

    # Parse the plantuml file
    regex.parse_uml(archivo_plantuml)

    # Get results observers
    result_printer = api.results_observers['printer']()
    result_csv = api.results_observers['csv']()
    result_composable = api.results_observers['composable'](
        [result_printer, result_csv])

    # Get result queries
    cypher = api.result_queries['cypher'](result_composable)

    # Count the coupling of the class
    cypher.resolve_query()

    # Delete the plantuml file
    cpp_generator.delete_plantuml(archivo_plantuml)


# Execute the main logic
if __name__ == "__main__":
    Main.execute()
