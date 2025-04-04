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

