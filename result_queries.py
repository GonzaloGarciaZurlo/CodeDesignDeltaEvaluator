"""
module that contains the PUML_Parser abstract class
"""
from abc import ABC, abstractmethod
from result_observer import ResultObserver


class ResultQueries(ABC):
    """
    Abstract class that represents a resolver queries.
    """
    def __init__(self, observer: ResultObserver) -> None:
        self.observer = observer

    @abstractmethod
    def resolve_query(self, query: str) -> None:
        "Abstract method that must be implemented by each resolver"
