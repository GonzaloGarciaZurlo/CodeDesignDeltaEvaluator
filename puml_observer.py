"""
module that contains the Observer abstract class for parsers   
"""
from abc import ABC, abstractmethod


class Observer(ABC):
    """
    Abstract class that represents an observer.
    """
    @abstractmethod
    def open_observer(self) -> None:
        """Event triggered when the observer is opened."""

    @abstractmethod
    def close_observer(self) -> None:
        """Event triggered when the observer is closed."""

    @abstractmethod
    def on_class_found(self, class_name: str, kind: str, label: str) -> None:
        """Event triggered when a class is found."""

    @abstractmethod
    def on_relation_found(self, class1: str, class2: str, relation: str, label: str) -> None:
        """Event triggered when a relation is found."""

    @abstractmethod
    def on_package_found(self, package_name: str, classes: list, label: str) -> None:
        """Event triggered when a package is found."""