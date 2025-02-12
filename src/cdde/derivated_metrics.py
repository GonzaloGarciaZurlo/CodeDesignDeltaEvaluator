"""
This module contains functions for handling derivated metrics.
"""
from src.cdde.eval import safe_eval


class DerivateMetrics():
    """
    This class is responsible for calculating the derivated metrics.
    """

    def get_file_path(self) -> str:
        """
        Get the file path of the queries.
        """
        return "../queries/derivate.yml"

    def run_derivate(self, list_of_queries: list, results: dict, argument: str = "") -> tuple[float, str]:
        """
        Run the list of derivate queries.
        """
        for query in list_of_queries:

            results['package'] = argument

            formula = query['query']
            result = safe_eval(formula, results)
            metric_name = query['metric']

            return (result, metric_name)
