"""
This module contains functions for handling database queries.
"""
from neo4j import GraphDatabase


class Neo4jCoupling:
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(
            self.uri, auth=("neo4j", "holacomoestas"))

    def get_class_coupling(self, class_name: str) -> dict:
        """
        Gets the coupling of a class.
        """
        with self.driver.session() as session:
            # Llama a las funciones de acoplamiento aferente y deferente
            acoplamiento = session.read_transaction(
                self._calculate_coupling, class_name)
            return acoplamiento

    @staticmethod
    def _calculate_coupling(tx, class_name: str) -> dict:
        """
        Calculates the efferent and afferent coupling of a class.
        """
        query = """
        MATCH (c:Class {name: $class_name})
        OPTIONAL MATCH (external:Class)-[r1]->(c)
        OPTIONAL MATCH (c)-[r2]->(dependent:Class)
        RETURN count(r1) AS acoplamiento_aferente, count(r2) AS acoplamiento_deferente
        """
        result = tx.run(query, class_name=class_name).single()
        return {
            'acoplamiento_aferente de ' + class_name: result["acoplamiento_aferente"],
            'acoplamiento_deferente de ' + class_name: result["acoplamiento_deferente"]
        }
