"""
This module contains the composable observer, 
Selected from 1 or more of the possible observers
"""
from typing import List
from overrides import override
from parser_puml.puml_observer import Observer


class Composable(Observer):
    """
    Selected from 1 or more of the possible observers
    """

    def __init__(self, observers: List[Observer]) -> None:
        self.observers = observers

    @override
    def on_class_found(self, class_name: str) -> None:
        for observer in self.observers:
            observer.on_class_found(class_name)

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        for observer in self.observers:
            observer.on_relation_found(class1, class2, relation)
