"""
This module contains the ResultComposable observer, 
Selected from 1 or more of the possible observers.
"""
from typing import List
from overrides import override
from src.cdde.addons_api import CddeAPI
from src.cdde.metric_result_observer import ResultObserver


class ResultComposable(ResultObserver):
    """
    Selected from 1 or more of the possible observers.
    """

    def __init__(self, observers: List[ResultObserver]) -> None:
        self.observers = observers

    @override
    def on_result_metric_found(self, result: int, kind: str, class_name) -> None:
        """
        Notifies the observers that a result was found.
        """
        for observer in self.observers:
            observer.on_result_metric_found(result, kind, class_name)

    @override
    def on_result_data_found(self, result: str, kind: str) -> None:
        """
        Notifies the observers that a result was found.
        """
        for observer in self.observers:
            observer.on_result_data_found(result, kind)

    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened.
        """
        for observer in self.observers:
            observer.open_observer()

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """
        for observer in self.observers:
            observer.close_observer()


def init_module(api: CddeAPI) -> None:
    """
    Initializes the module on the API.
    """
    api.register_result_observer('res_composable', ResultComposable)
