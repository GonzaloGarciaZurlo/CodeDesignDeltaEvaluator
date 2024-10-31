"""
This module contains functions for handling database queries.
"""
from neo4j import GraphDatabase, Transaction
from overrides import override
from result_queries import ResultQueries
from api import CddeAPI


class QueriesCypher(ResultQueries):
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self, observer) -> None:
        super().__init__(observer)
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(
            self.uri, auth=("neo4j", "holacomoestas"))

    @override
    def resolve_query(self, query: str) -> None:
        """
        Resolves the query.
        """
        class_name = query
        self.observer.open_observer()
        self.get_class_coupling(class_name)
        self.observer.close_observer()

    def get_class_coupling(self, class_name: str) -> None:
        """
        Gets the coupling of a class.
        """
        with self.driver.session() as session:
            session.read_transaction(self._calculate_coupling, class_name)

    def _calculate_coupling(self, tx: Transaction, class_name: str) -> None:
        """
        Calculates the efferent and afferent coupling of a class.
        """
        query = """
        MATCH (c:Class {name: $class_name})
        OPTIONAL MATCH (external:Class)-[r1]->(c)
        OPTIONAL MATCH (c)-[r2]->(dependent:Class)
        RETURN count(r1) AS afferent_coupling, count(r2) AS deferent_coupling
        """
        result = tx.run(query, class_name=class_name).single()

        coupling = {
            'afferent coupling of class ' + class_name: result["afferent_coupling"],
            'deferent coupling of class ' + class_name: result["deferent_coupling"]
        }
        self.observer.on_result_found(str(coupling), "coupling")


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_queries('cypher', QueriesCypher)
