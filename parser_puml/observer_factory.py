"""
Factory class that creates the parser object based on the selected implementation.
"""
from parser_puml import puml_observer, printer, composable_observer
from relationship_db import create_db_neo4j

# list of observers
PRINTER = "printer"
NEO4J = "neo4j"
COMPOSABLE = "composable"


class ObserverFactory():
    """
    Class that creates the parser object based on the selected implementation.
    """

    @staticmethod
    def create_observer(name: str, observers=[]) -> puml_observer.Observer:
        """
        Creates the parser object based on the selected implementation.
        """
        if name == PRINTER:
            return printer.Printer()
        elif name == NEO4J:
            return create_db_neo4j.Neo4j()
        elif name == COMPOSABLE:
            return composable_observer.Composable(observers)
        else:
            print("Invalid observer")
