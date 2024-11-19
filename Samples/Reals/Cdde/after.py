
from abc import ABC, abstractmethod
from puml_observer import Observer
import subprocess
from result_observer import ResultObserver


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
    def on_class_found(self, class_name: str, kind: str, label: str) -> None:
        """Event triggered when a class is found."""

    @abstractmethod
    def on_relation_found(self, class1: str, class2: str, relation: str, label: str) -> None:
        """Event triggered when a relation is found."""


class PumlParser(ABC):
    """
    Abstract class that represents a PUML parser.
    """

    def __init__(self, observer: Observer, label: str) -> None:
        self.observer = observer
        self.label = label

    @abstractmethod
    def parse_uml(self, file: str) -> None:
        """
        Parse the PUML file, and set label (after or before).
        """


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
    def on_result_metric_found(self, result: str, kind: str, class_name: str) -> None:
        """Event triggered when a metric is found."""

    @abstractmethod
    def on_result_data_found(self, result: str, kind: str) -> None:
        """Event triggered when a structure data is found."""


class ResultQueries(ABC):
    """
    Abstract class that represents a resolver queries.
    """

    def __init__(self, observer: ResultObserver) -> None:
        self.observer = observer

    @abstractmethod
    def resolve_query(self) -> None:
        "Abstract method that must be implemented by each resolver"


class PumlGenerator(ABC):
    """
    Abstract class for PlantUML generators.
    """

    @abstractmethod
    def generate_plantuml(self, file_path: str) -> str:
        """
        Generate the PlantUML file.
        """

    def delete_plantuml(self, uml_path: str) -> None:
        """
        delete the plantuml file
        """
        try:
            subprocess.run(['rm', '-rf', uml_path], check=True)

        except subprocess.CalledProcessError:
            print("Error: Failed to delete .plantuml file.")
