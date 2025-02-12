"""
This module contains functions for handling derivated metrics.
"""
from overrides import override
from src.cdde.eval import safe_eval
from src.cdde.metric_generator import MetricGenerator


class DerivateMetrics(MetricGenerator):
    """
    This class is responsible for calculating the derivated metrics.
    """

    @override
    def get_file_path(self) -> str:
        """
        Get the file path of the queries.
        """
        return "../queries/derivate.yml"

    @override
    def run_metrics(self, query: str, results: dict = {}) -> float:
        """
        Run the list of derivate queries.
        """
        result = safe_eval(query, results)
        return result

    @override
    def send_result(self, result: float, kind_metrics: str, metric_name: str) -> None:
        """
        Send the results to the observer.
        """
        self.observer.on_result_metric_found(result, kind_metrics, metric_name)
