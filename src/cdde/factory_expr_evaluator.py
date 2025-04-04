from src.cdde.expr_evaluator import ExprEvaluator
from src.cdde.addons_api import CddeAPI

class FactoryExprEvaluator:
    """
    Factory class to create an expression evaluator.
    """

    @staticmethod
    def create_evaluator(evaluator_type: str, api: CddeAPI) -> ExprEvaluator:
        """
        Create an expression evaluator.
        """
        return api.expr_evaluator[evaluator_type]()