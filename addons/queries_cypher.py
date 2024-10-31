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
    def resolve_query(self) -> None:
        """
        Resolves the query.
        """
        class_name = ""
        self.observer.open_observer()
        classes = self.get_all_classes()
        for class_name in classes:
            self.get_class_coupling(class_name)
        self.observer.close_observer()

    def get_all_classes(self) -> list:
        """
        Gets all classes in the database.
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_classes)
        return result

    def _get_all_classes(self, tx: Transaction) -> list:
        """
        Helper function to get all classes in the database.
        """
        query = "MATCH (c:Class) RETURN c.name AS name"
        result = tx.run(query)
        return [record["name"] for record in result]

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
            class_name + ' afferent coupling': result["afferent_coupling"],
            class_name + ' deferent coupling' + class_name: result["deferent_coupling"]
        }
        self.observer.on_result_found(str(coupling), "coupling")


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_queries('cypher', QueriesCypher)
