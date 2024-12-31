"""
This module contains the Printer class, 
which is an Observer that prints the information it receives.
"""
from overrides import override
from api import CddeAPI
from puml_observer import Observer


class Printer(Observer):
    """
    Observer that prints the information it receives
    """
    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened
        """
        print("Parser:")
        print("--------------------------------")

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed
        """
        print("--------------------------------")

    @override
    def on_class_found(self, class_name: str, kind, label: str) -> None:
        """
        Print the class found
        """
        print(f"{kind} found: {label}_{class_name}")

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str, label: str) -> None:
        """
        Print the relationship found
        """
        print(f"Relationship found: ({relation}) {label}_{class1} --> {label}_{class2}")

    @override
    def on_package_found(self, package_name: str, classes: list, label: str) -> None:
        """
        Print the package found
        """
        print(f"Package found: {label}_{package_name} with classes: {classes}")


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('printer', Printer)
