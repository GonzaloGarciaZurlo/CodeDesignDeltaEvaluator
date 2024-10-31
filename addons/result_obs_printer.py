"""
This module contains the Printer class, 
which is an Observer that prints the information it receives.
"""
from overrides import override
from api import CddeAPI
from result_observer import ResultObserver

class ResultPrinter(ResultObserver):
    """
    Observer that prints the information it receives
    """
    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened
        """
        print("Results:")
        print("--------------------------------")

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed
        """
        print("--------------------------------")

    @override
    def on_result_found(self, result: str) -> None:
        """
        Print the result found
        """
        print(f"Result found: {result}")

def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_observer('printer', ResultPrinter)
