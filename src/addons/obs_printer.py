"""
This module contains the Printer class, 
which is an Observer that prints the information it receives.
"""
from overrides import override
from src.cdde.addons_api import CddeAPI
from src.cdde.puml_observer import Observer, Modes, ClassKind, Relationship

class Printer(Observer):
    """
    Observer that prints the information it receives.
    """

    def __init__(self) -> None:
        self.mode: Modes

    @override
    def set_mode(self, mode: Modes) -> None:
        """
        Set the mode of the observer.
        """
        print(f"Mode set to: {mode.value}")
        self.mode = mode

    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened.
        """
        print("Parser:")
        print("--------------------------------")

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """
        print("--------------------------------")

    @override
    def on_class_found(self, class_name: str, kind: ClassKind) -> None:
        """
        Print the class found.
        """
        print(f"{kind.value} found: {self.mode.value}_{class_name}")

    @override
    def on_relation_found(self, class1: str, class2: str, relation: Relationship) -> None:
        """
        Print the relationship found.
        """
        print(f"Relationship found: ({relation.name}) {
              self.mode.value}_{class1} --> {self.mode.value}_{class2}")

    @override
    def on_package_found(self, package_name: str, classes: list) -> None:
        """
        Print the package found.
        """
        print(f"Package found: {self.mode.value}_{
              package_name} with classes: {classes}")


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('printer', Printer)
