"""
This module contains functions for handling database queries.
"""
from neo4j import GraphDatabase
from overrides import override
from src.cdde.expr_evaluator import ExprEvaluator, MetricType
from src.cdde.addons_api import CddeAPI


class QueriesCypher(ExprEvaluator):
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self) -> None:
        self.uri = self._get_uri()
        self.driver = GraphDatabase.driver(self.uri, auth=None)
        self.path = "src/queries/cypher.yml"

    def _get_uri(self) -> str:
        """
        Get the URI of the Neo4j database in the uri.txt file.
        """
        try:
            with open("uri.txt", 'r', encoding="utf-8") as file:
                return file.read().strip()
        except:
            return "bolt://localhost:7689"

    @override
    def eval(self,
             expr: str,
             arguments: dict,  # type: ignore
             results: dict) -> MetricType:  # type: ignore
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        with self.driver.session() as session:
            record = session.execute_read(
                lambda tx: tx.run(expr, **arguments).single()
            )
        if record is None:
            return 0
        value = record[0]
        return 0 if value is None else value  # type: ignore


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_expr_evaluator('cypher-metrics', QueriesCypher)
