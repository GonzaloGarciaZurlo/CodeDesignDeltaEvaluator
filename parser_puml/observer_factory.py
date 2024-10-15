"""
Factory class that creates the observer object based on the selected implementation.
"""
from relationship_db import create_db_neo4j
from parser_puml import puml_observer, printer, composable_observer

# list of observers
PRINTER = "printer"
NEO4J = "neo4j"
COMPOSABLE = "composable"


class ObserverFactory():
    """
    Class that creates the observer object based on the selected implementation.
    """

    @staticmethod
    def create_observer(name: str, observers=[]) -> puml_observer.Observer:
        """
        Creates the observer object based on the selected implementation.
        """
        if name == PRINTER:
            return printer.Printer()
        if name == NEO4J:
            return create_db_neo4j.Neo4j()
        if name == COMPOSABLE:
            return composable_observer.Composable(observers)
        print("Invalid observer")
        return None
