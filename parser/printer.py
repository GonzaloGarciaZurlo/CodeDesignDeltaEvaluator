"""
This module contains the Printer class, 
which is an Observer that prints the information it receives.
"""
from parser.puml_observer import Observer
from overrides import override


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
