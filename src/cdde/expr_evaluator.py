from abc import ABC, abstractmethod

MetricType = float


class ExprEvaluator(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def eval(self,
             expr: str,
             arguments: dict[str, str] = {},
             results: dict[str, str | float] = {}) -> MetricType:
        """
        Evaluate the expression.
        """
