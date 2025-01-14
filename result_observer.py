"""
module that contains the Observer abstract class for results of queries
"""
from abc import ABC, abstractmethod


class ResultObserver(ABC):
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
    def on_result_metric_found(self, result: int, kind: str, class_name: str) -> None:
        """Event triggered when a metric is found."""

    @abstractmethod
    def on_result_data_found(self, result: str, kind: str) -> None:
        """Event triggered when a structure data is found."""
