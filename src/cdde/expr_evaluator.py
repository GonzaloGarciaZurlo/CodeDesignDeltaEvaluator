""" Abstract class for evaluating expressions. """
from abc import ABC, abstractmethod

MetricType = float


class ExprEvaluator(ABC):
    """
    Abstract class for evaluating expressions.
    """
    @abstractmethod
    def eval(self,
             expr: str,
             arguments: dict[str, str],
             results: dict[str, str | float]) -> MetricType:
        """
        Evaluate the expression.
        """
