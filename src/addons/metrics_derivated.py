"""
This module contains functions for handling derivated metrics.
"""
from overrides import override
from src.cdde.eval import safe_eval
from src.cdde.expr_evaluator import ExprEvaluator, MetricType
from src.cdde.addons_api import CddeAPI


class DerivateMetrics(ExprEvaluator):
    """
    This class is responsible for calculating the derivated metrics.
    """

    @override
    def eval(self,
             expr: str,
             arguments: dict[str, str] = {},
             results: dict[str, str | float] = {}) -> MetricType:
        """
        Evaluate an expression.
        """
        return safe_eval(expr, results)


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_expr_evaluator('derivate-metrics', DerivateMetrics)
