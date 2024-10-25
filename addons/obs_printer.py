"""
This module contains the Printer class, 
which is an Observer that prints the information it receives.
"""
from overrides import override
from CodeDesignDeltaEvaluator.factories.puml_observer import Observer
from CddeAPI import CddeAPI

class Printer(Observer):
    """
    Observer that prints the information it receives
    """
    @override
    def on_class_found(self, class_name: str) -> None:
        print(f"Class found: {class_name}")

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        print(f"Relationship found: {relation} : {class1} --> {class2}")

def init_module(api: CddeAPI) -> None:
    api.register_puml_observer('printer', Printer())