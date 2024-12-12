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

    db_neo4j.delete_all()

    # Get parsers
    regex_before = api.parsers['regex'](composable, "before")
    regex_after = api.parsers['regex'](composable, "after")
    parsimonious_before = api.parsers['parsimonius'](composable, "before")
    parsimonius_after = api.parsers['parsimonius'](composable, "after")

    # Examples files
    archivo_go = "Samples/Simple/double derivative/after.go"
    archivo_py = "Samples/SOLID+LoD/I/ISP_P.py"
    

    pylint_before = "Samples/Reals/pylint/before.py"
    pylint_after = "Samples/Reals/pylint/after.py"
    openMW_before = "Samples/Reals/OpenMW/before.cpp"
    openMW_after = "Samples/Reals/OpenMW/after.cpp"
    cdde_before = "Samples/Reals/Cdde/before.py"
    cdde_after = "Samples/Reals/Cdde/after.py"

    # python examples
    complex_example = "Samples/Complex/python/before"
    base_class_change_before = "Samples/Simple/base-class-change/before"
    base_class_change_after = "Samples/Simple/base-class-change/after"

    # c++ examples
    derivate_to_composition_cpp_before = "Samples/Simple/derivative-to-composition/before"
    derivate_to_composition_cpp_after = "Samples/Simple/derivative-to-composition/after"
    complex_example_cpp_before = "Samples/Complex/c++/before"
    complex_example_cpp_after = "Samples/Complex/c++/after"

    # Generate the plantuml file
    archivo_plantuml_before = py_generator.generate_plantuml(
        base_class_change_before)
    archivo_plantuml_after = py_generator.generate_plantuml(
        base_class_change_after)

    # Parse the plantuml file
    regex_before.parse_uml(archivo_plantuml_before)
    regex_after.parse_uml(archivo_plantuml_after)

    # Get results observers
    result_printer = api.results_observers['printer']()
    result_csv = api.results_observers['csv']()
    result_json = api.results_observers['json']()
    result_composable = api.results_observers['composable'](
        [result_csv, result_json])

    # Get result queries
    cypher = api.result_queries['cypher'](result_composable)

    # Count the coupling of the class
    cypher.resolve_query()

    # Delete the plantuml file
    py_generator.delete_plantuml(archivo_plantuml_before)
    py_generator.delete_plantuml(archivo_plantuml_after)


# Execute the main logic
if __name__ == "__main__":
    Main.execute()
