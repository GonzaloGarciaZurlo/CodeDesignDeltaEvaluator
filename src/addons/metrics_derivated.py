"""
This module contains functions for handling derived metrics.
"""
from overrides import override
from src.cdde.eval import safe_eval
from src.cdde.expr_evaluator import ExprEvaluator, MetricType
from src.cdde.addons_api import CddeAPI


class DerivedMetrics(ExprEvaluator):
    """
    This class is responsible for calculating the derived metrics.
    """

    @override
    def eval(self,
             expr: str,
             arguments: dict[str, str],    # type: ignore
             results: dict[str, str | float]) -> MetricType:   # type: ignore
        """
        Evaluate an expression.
        """
        return safe_eval(expr, results)


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_expr_evaluator('derived-metrics', DerivedMetrics)
