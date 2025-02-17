"""
This module contains functions for handling derivated metrics.
"""
from overrides import override
from src.cdde.eval import safe_eval
from src.cdde.metric_generator import MetricGenerator
from src.cdde.addons_api import CddeAPI


class DerivateMetrics(MetricGenerator):
    """
    This class is responsible for calculating the derivated metrics.
    """

    @override
    def get_file_path(self) -> str:
        """
        Get the file path of the queries.
        """
        return "src/queries/derivate_metrics.yml"

    @override
    def run_metrics(self, query: str, argument: dict = {}) -> float:
        """
        Run the list of derivate queries.
        """
        result = safe_eval(query, argument)
        return result


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_metric_generator('derivate', DerivateMetrics)
