"""
Module that contains the MetricGenerator abstract class
"""
from abc import ABC, abstractmethod
from .metric_result_observer import ResultObserver


class MetricGenerator(ABC):
    """
    Abstract class that represents a MetricGenerator queries.
    """
    @abstractmethod
    def run_metrics(self, query: str, argument: dict = {}) -> float:
        """
        Run the query in the language of the database.
        """

    @abstractmethod
    def get_file_path(self) -> str:
        """
        Get the file path of the queries.
        """


class AddonsMetricGenerator(MetricGenerator):
    """
    Abstract class that represents a AddonsMetricGenerator queries.
    """
    @abstractmethod
    def get_all_classes(self) -> list:
        """
        Obtains all classes in the database.
        """

    @abstractmethod
    def get_all_relations(self, class_name: str) -> list[tuple]:
        """
        Obtains all relations of a class.
        """

    @abstractmethod
    def get_all_packages(self) -> list:
        """
        Obtains all packages in the database.
        """

    @abstractmethod
    def set_packages(self, class_name: str) -> None:
        """
        Set the packages of a class.
        """