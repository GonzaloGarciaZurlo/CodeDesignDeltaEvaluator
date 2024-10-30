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
    def on_class_found(self, class_name: str, kind) -> None:
        """
        Print the class found
        """
        print(f"{kind} found: {class_name}")

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        """
        Print the relationship found
        """
        print(f"Relationship found: {relation} : {class1} --> {class2}")



def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('printer', Printer)
