"""
Module that contains the MetricGenerator abstract class
"""
from abc import ABC, abstractmethod
import yaml


class MetricGenerator(ABC):
    """
    Abstract class that represents a MetricGenerator queries.
    """
    def __init__(self):
        """
        Initialize the MetricGenerator.
        """
        self.path = None

    def _load_queries(self, file_path: str) -> dict:
        """
        Transforms a yaml file into a dictionary.
        The dictionary contains all queries in the shape:
        metrics-generator: ...
        snaphot-metrics:
            global:[...]
            per-class:[...]
            per-package:[...]
        delta-metrics:
            global:[...]
            per-class:[...]
            per-package:[...]
        """
        with open(file_path, 'r', encoding="utf-8") as file:
            return yaml.load(file, Loader=yaml.SafeLoader)

    @abstractmethod
    def run_metric(self,
                   query: str,
                   argument: dict = {},
                   results: dict = {}) -> float:
        """
        Run the query in the language of the database.
        """

    def get_queries(self) -> dict:
        """
        Get all queries of your file.
        """
        try:
            queries = self._load_queries(self.path)
            queries.pop('metrics-generator')
            return queries
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return {}


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
