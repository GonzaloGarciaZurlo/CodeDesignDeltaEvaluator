"""
This module contains functions for handling database queries.
"""
from neo4j import GraphDatabase, Transaction
from overrides import override
from src.cdde.metric_generator import AddonsMetricGenerator
from src.cdde.addons_api import CddeAPI


class QueriesCypher(AddonsMetricGenerator):
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self) -> None:
        self.uri = "bolt://localhost:7689"
        self.driver = GraphDatabase.driver(self.uri, auth=None)
        self.packages = []

    @override
    def get_file_path(self) -> str:
        """
        Get the file path of the queries.
        """
        return "src/queries/cypher.yml"

    @override
    def run_metrics(self, query: str, argument: dict = {}) -> float:
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        with self.driver.session() as session:
            result = session.execute_read(
                lambda tx: tx.run(query, **argument).single()[0])

        return result

    @override
    def get_all_classes(self) -> list:
        """
        Gets all classes in the database.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_classes)
        return result

    def _get_all_classes(self, tx: Transaction) -> list:
        """
        Helper function to get all classes in the database.
        """
        query = """
                MATCH (c) RETURN c.name AS name
                """
        result = tx.run(query)
        return [record["name"] for record in result]

    @override
    def get_all_relations(self, class_name: str) -> list[tuple]:
        """
        Gets all relations of a class.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_relations, class_name)
        return result

    def _get_all_relations(self, tx: Transaction,
                           class_name: str) -> list[tuple]:
        """
        Helper function to get all relations of a class.
        """
        query = """
                MATCH (c {name: $class_name})-[r]->(dependent)
                RETURN type(r) AS relation, dependent.name AS dependent
                """
        result = tx.run(query, class_name=class_name)
        r = []
        for record in result:
            r.append((record["relation"], record["dependent"]))
        return r

    @override
    def set_packages(self, class_name: str) -> None:
        """
        Sets all of the packages in the database.
        """
        with self.driver.session() as session:
            session.execute_read(self._set_packages, class_name)

    def _set_packages(self, tx: Transaction, class_name: str) -> None:
        """
        Helper function to get all of the packages in the database.
        """
        query = """
                MATCH (c {name: $class_name})
                RETURN c.package AS package
                """
        result = tx.run(query, class_name=class_name).single()[0]
        if result not in self.packages:
            self.packages.append(result)
        if self.packages == [None]:
            self.packages = []

    @override
    def get_all_packages(self) -> list:
        """
        Gets all packages in the database.
        """
        return self.packages


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_metric_generator('cypher', QueriesCypher)
