""" Abstract class that represents a design database. """
from abc import ABC, abstractmethod
from typing import NamedTuple
from src.cdde.puml_observer import Relationship


class RelationshipType(NamedTuple):
    """
    Class that represents a relationship between two classes.
    """
    class1: str
    class2: str
    relation: Relationship


class DesignDB(ABC):
    """
    Abstract class that represents a design database.
    """
    @abstractmethod
    def get_all_classes(self) -> list[str]:
        """
        Obtains all classes in the database.
        """

    @abstractmethod
    def get_class_per_package(self, package_name: str) -> list[str]:
        """
        Obtains all classes in a package.
        """

    @abstractmethod
    def get_methods_per_class(self, class_name: str) -> list[str]:
        """
        Obtains all methods of a class.
        """

    @abstractmethod
    def get_all_relations(self, class_name: str) -> list[RelationshipType]:
        """
        Obtains all relations of a class.
        """

    @abstractmethod
    def get_all_packages(self) -> list[str]:
        """
        Obtains all packages in the database.
        """

    @abstractmethod
    def set_packages(self, class_name: str) -> None:
        """
        Sets the packages of a class.
        """
