"""
Factory class that creates the observer object based on the selected implementation.
"""
from CodeDesignDeltaEvaluator.addons import obs_composable
from CodeDesignDeltaEvaluator.factories import puml_observer
from CodeDesignDeltaEvaluator.addons import obs_db_neo4j
from CodeDesignDeltaEvaluator.addons import obs_printer

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
            return obs_printer.Printer()
        if name == NEO4J:
            return obs_db_neo4j.Neo4j()
        if name == COMPOSABLE:
            return obs_composable.Composable(observers)
        print("Invalid observer")
        return None
