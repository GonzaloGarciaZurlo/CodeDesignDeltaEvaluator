"""
Module that contains the MetricGenerator abstract class
"""
from abc import ABC, abstractmethod
from .metric_result_observer import ResultObserver


class MetricGenerator(ABC):
    """
    Abstract class that represents a MetricGenerator queries.
    """

    def __init__(self, observer: ResultObserver) -> None:
        self.observer = observer

    @abstractmethod
    def send_result(self, result: float, kind_metrics: str, metric_name: str) -> None:
        """
        Send the results to the observer.
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

    @abstractmethod
    def get_all_classes(self) -> list:
        """
        Obtains all classes in the database.
        """

    @abstractmethod
    def get_all_relations(self) -> None:
        """
        Obtains all relations of a class.
        """

    @abstractmethod
    def get_all_packages(self) -> None:
        """
        Obtains all packages in the database.
        """
