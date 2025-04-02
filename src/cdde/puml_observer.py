"""
module that contains the Observer abstract class for parsers   
"""
from abc import ABC, abstractmethod
from enum import StrEnum


class Modes(StrEnum):
    Before = 'before'
    After = 'after'

class Relationship(StrEnum):
    inheritance = '--|>'
    implementation = '..|>'
    dependency = '-->'
    composition = '--*'
    aggregation = '--o'
    association = '--'

class ClassKind(StrEnum):
    Class = 'class'
    Interface = 'interface'
    Abstract = 'abstract'


class Observer(ABC):
    """
    Abstract class that represents an observer.
    """
    @abstractmethod
    def set_mode(self, mode: Modes) -> None:
        """
        Sets the mode of the observer.
        """

    @abstractmethod
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened.
        """

    @abstractmethod
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """

    @abstractmethod
    def on_class_found(self, class_name: str, kind: ClassKind) -> None:
        """
        Event triggered when a class is found.
        """

    @abstractmethod
    def on_relation_found(self, class1: str, class2: str, relation: Relationship) -> None:
        """
        Event triggered when a relation is found.
        """

    @abstractmethod
    def on_package_found(self, package_name: str, classes: list) -> None:
        """
        Event triggered when a package is found.
        """
