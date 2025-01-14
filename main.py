"""
This module handles the main execution flow of the application.
"""
from api import CddeAPI
from git_clone import GitClone


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

    # Get Filter
    filter = api.observers['filter'](composable)
    filter2 = api.observers['filter'](composable)

    # Get parsers
    parsimonious_before = api.parsers['parsimonius'](filter, "before")
    parsimonius_after = api.parsers['parsimonius'](filter2, "after")

    # go examples
    double_derivative_before = "Samples/Simple/double-derivative/before"
    double_derivative_after = "Samples/Simple/double-derivative/after"

    # python examples
    complex_example = "Samples/Complex/python/before"
    ISP_P = "Samples/SOLID+LoD/I/ISP_P.py"
    base_class_change_before = "Samples/Simple/base-class-change/before"
    base_class_change_after = "Samples/Simple/base-class-change/after"

    # c++ examples
    derivate_to_composition_before = "Samples/Simple/derivative-to-composition/before"
    derivate_to_composition_after = "Samples/Simple/derivative-to-composition/after"
    complex_example_before = "Samples/Complex/c++/before"
    complex_example_after = "Samples/Complex/c++/after"
    complex_example_after_base_class_change = "Samples/Complex/c++/after_base_class_change"

    # Git examples
    git_clone_go = GitClone(
        "https://github.com/jfeliu007/goplantuml", 168)  # GO (none changes)
    # git_clone_cpp = GitClone(
    #   "https://github.com/jfeliu007/goplantuml", 145) # GO (many changes)

    git_clone_go.run()
    # Temporal directories
    before = git_clone_go.before_dir
    after = git_clone_go.after_dir

    # Generate the plantuml file
    archivo_plantuml_before = go_generator.generate_plantuml(
        before)
    archivo_plantuml_after = go_generator.generate_plantuml(
        after)

    # Parse the plantuml file
    parsimonious_before.parse_uml(archivo_plantuml_before)
    parsimonius_after.parse_uml(archivo_plantuml_after)

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
    go_generator.delete_plantuml(archivo_plantuml_before)
    go_generator.delete_plantuml(archivo_plantuml_after)

    # Delete the temporary directories
    git_clone_go.delete_dir()


# Execute the main logic
if __name__ == "__main__":
    Main.execute()
