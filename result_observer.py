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
    def on_result_found(self, result: str, kind: str) -> None:
        """Event triggered when a result is found."""
