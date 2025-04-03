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

    def __init__(self):
        self.path = "src/queries/derivate_metrics.yml"

    @override
    def run_metric(self,
                   query: str,
                   argument: dict = {},
                   results: dict = {}) -> float:
        """
        Run the list of derivate queries.
        """
        result = safe_eval(query, results)
        return result


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_metric_generator('derivate', DerivateMetrics)
