"""
This module contains the ResultPrinter class, 
which is an Observer that prints the information it receives.
"""
from overrides import override
from src.cdde.api import CddeAPI
from src.cdde.result_observer import ResultObserver


class ResultPrinter(ResultObserver):
    """
    Observer that prints the information it receives.
    """
    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened.
        """
        print("Results:")
        print("--------------------------------")

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """
        print("--------------------------------")

    @override
    def on_result_metric_found(self, result: int, kind: str, class_name) -> None:
        """
        Print the result found.
        """
        print(f"{class_name} {kind}: {result}")

    @override
    def on_result_data_found(self, result: str, kind: str) -> None:
        """
        Print the result found.
        """
        print(f"{kind}: {result}")


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_observer('res_printer', ResultPrinter)
