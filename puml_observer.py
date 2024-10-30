"""
module that contains the Observer abstract class   
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
    def on_class_found(self, class_name: str, kind: str) -> None:
        """Event triggered when a class is found."""

    @abstractmethod
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        """Event triggered when a relation is found."""
