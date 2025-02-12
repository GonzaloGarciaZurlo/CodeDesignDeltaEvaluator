"""
This module contains functions for handling database queries.
"""
from neo4j import GraphDatabase, Transaction
from overrides import override
from cdde.metric_generator import MetricGenerator
from cdde.addons_api import CddeAPI
from src.cdde.eval import safe_eval
from cdde.metric_result_observer import ResultObserver


class QueriesCypher(MetricGenerator):
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self, observer: ResultObserver) -> None:
        super().__init__(observer)
        self.uri = "bolt://localhost:7689"
        self.driver = GraphDatabase.driver(
            self.uri, auth=None)

    @override
    def get_file_path(self) -> str:
        """
        Get the file path of the queries.
        """
        return "../queries/cypher.yml"

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
    def send_result(self, result: float, kind_metrics: str, metric_name: str) -> None:
        """
        Send the results to the observer.
        """
        self.observer.on_result_metric_found(result, kind_metrics, metric_name)

    @override
    def get_all_classes(self) -> list:
        """
        Gets all classes in the database.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_classes)
            self.observer.on_result_data_found(str(result), "classes")
            self.observer.on_result_metric_found(
                len(result), "classes", "total")
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
    def get_all_relations(self, class_name: str) -> None:
        """
        Gets all relations of a class.
        """
        with self.driver.session() as session:
            session.execute_read(self._get_all_relations, class_name)

    def _get_all_relations(self, tx: Transaction, class_name: str) -> None:
        """
        Helper function to get all relations of a class.
        """
        query = """
                MATCH (c {name: $class_name})-[r]->(dependent)
                RETURN type(r) AS relation, dependent.name AS dependent
                """
        result = tx.run(query, class_name=class_name)
        for record in result:
            self.observer.on_result_data_found(
                str(class_name)+' --> '+str(record['dependent']), str(record["relation"]))

    @override
    def get_all_packages(self, class_name: str) -> None:
        """
        Sets all of the packages in the database.
        """
        with self.driver.session() as session:
            session.execute_read(self._get_packages, class_name)

    def _get_packages(self, tx: Transaction, class_name: str) -> None:
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


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_queries('cypher', QueriesCypher)
