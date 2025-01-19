"""
This module contains the composable observer, 
Selected from 1 or more of the possible observers.
"""
from typing import List
from overrides import override
from src.CddE.api import CddeAPI
from src.CddE.puml_observer import Observer


class Composable(Observer):
    """
    Selected from 1 or more of the possible observers.
    """

    def __init__(self, observers: List[Observer]) -> None:
        self.observers = observers

    @override
    def set_mode(self, mode: str) -> None:
        """
        Sets the mode of the observer.
        """
        for observer in self.observers:
            observer.set_mode(mode)

    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened.
        """
        for observer in self.observers:
            observer.open_observer()

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """
        for observer in self.observers:
            observer.close_observer()

    @override
    def on_class_found(self, class_name: str, kind: str) -> None:
        """
        Notifies the observers that a class was found.
        """
        for observer in self.observers:
            observer.on_class_found(class_name, kind)

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        """
        Notifies the observers that a relation between two classes was found.
        """
        for observer in self.observers:
            observer.on_relation_found(class1, class2, relation)

    @override
    def on_package_found(self, package_name: str, classes: list) -> None:
        """
        Notifies the observers that a package was found.
        """
        for observer in self.observers:
            observer.on_package_found(package_name, classes)


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_puml_observer('composable', Composable)
