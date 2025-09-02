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
        self.uri = "bolt://localhost:7689"
        self.driver = GraphDatabase.driver(self.uri, auth=None)
        self.path = "src/queries/cypher.yml"

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
