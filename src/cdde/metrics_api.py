"""
Module for the MetricsAPI class.
In this module we define the API for the metrics used in CodeDesignDeltaEvaluator.
"""
from abc import ABC, abstractmethod
from overrides import overrides
import yaml
from enum import Enum
from .metric_generator import MetricGenerator
from .derivated_metrics import DerivateMetrics


class TimeMetrics(Enum):
    SNAPSHOT_METRICS = 'snapshot-metrics'
    DELTA_METRICS = 'delta-metrics'


class KindMetrics(Enum):
    GLOBAL = 'global'
    PER_CLASS = 'per-class'
    PER_PACKAGE = 'per-package'


class MetricsAPI(ABC):
    """
    Interface for the metrics API.
    """

    @abstractmethod
    def add_global_metric(name: str, value: int) -> None:
        """
        Add a global metric to the API.
        """

    @abstractmethod
    def add_package_metric(name: str, package: str, value: int) -> None:
        """
        Add a package metric to the API.
        """

    @abstractmethod
    def add_class_metric(name: str, class_name: str, value: int) -> None:
        """
        Add a class metric to the API.
        """


class MetricsCalculator(MetricsAPI):
    """
    This class implements the MetricsAPI interface.
    """

    def __init__(self, metrics_generator: MetricGenerator) -> None:
        self.metrics_generator = metrics_generator
        self.derivate_metrics_generator = DerivateMetrics()
        self.classes: list = []
        self.relationships: list = []
        self.packages: list = []
        self.queries: dict = {}
        self.derivate_queries: dict = {}
        self.results: dict = {}

    def execute_all_metrics(self) -> None:
        """
        Executes all metrics.
        """
        self.queries = self._load_queries(
            self.metrics_generator.get_file_path())
        self.derivate_queries = self._load_queries(
            self.derivate_metrics_generator.get_file_path())

        self.classes = self.metrics_generator.get_all_classes()

        for class_name in self.classes:
            self.relationships = self.metrics_generator.get_all_relations(
                class_name)

        for package in self.packages:
            self.packages = self.metrics_generator.get_all_packages(package)

        self.set_metrics(self.metrics_generator)

    def _load_queries(self, file_path: str) -> dict:
        """
        Transforms a yaml file into a dictionary.
        The dictionary contains all queries in the shape:
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

    def set_metrics(self, metric_Generator: MetricGenerator) -> None:
        """
        Executes all cypher queries.
        """
        for time_metrics in TimeMetrics:
            for kind_metrics in KindMetrics:
                self.execute_metrics(
                    time_metrics, kind_metrics, metric_Generator)

        for time_metrics in TimeMetrics:
            for kind_metrics in KindMetrics:
                self.execute_derivate_queries(
                    time_metrics, kind_metrics)

    def execute_metrics(self, time_metrics: str, kind_metrics: str, metric_generator: MetricGenerator) -> None:
        """
        Execute all queries for a specific time and kind of metrics.
        """
        list_of_queries = self.queries[time_metrics][kind_metrics]
        if list_of_queries is None:
            return None
        if kind_metrics == KindMetrics.GLOBAL:
            self._run(list_of_queries, metric_generator)
        if kind_metrics == KindMetrics.PER_CLASS:
            for class_name in self.classes:
                self._run(list_of_queries, metric_generator, class_name)
        if kind_metrics == KindMetrics.PER_PACKAGE:
            for package_name in self.packages:
                self._run(list_of_queries, metric_generator, package_name)

    def _run(self, list_of_queries: list, kind_metrics: KindMetrics,
             metric_generator: MetricGenerator, argument: str = "") -> None:
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        for query in list_of_queries:
            params = self.set_params(query, argument, kind_metrics)
            result = metric_generator.run_metrics(query['query'], params)

            metric_name = self.set_metric_name(
                query['metric'], kind_metrics, argument)

            self.save_metric(metric_name, result, kind_metrics)
            self.metrics_generator.send_result(
                result, kind_metrics.value, metric_name)

    def set_params(self, query: dict, argument: str, kind_metrics: KindMetrics) -> dict:
        """
        Set the parameters of the query.
        """
        params = {}
        if kind_metrics == KindMetrics.PER_CLASS:
            params["class_name"] = argument
            kind = KindMetrics.PER_CLASS
        if kind_metrics == KindMetrics.PER_PACKAGE:
            params["package_name"] = argument
            kind = KindMetrics.PER_PACKAGE
        return params

    def execute_derivate_queries(self, time_metrics: TimeMetrics, kind_metrics: KindMetrics) -> None:
        """
        Execute all queries for a specific time and kind of metrics.
        """
        list_of_queries = self.derivate_queries[time_metrics][kind_metrics]
        if list_of_queries is None:
            return None
        if kind_metrics == KindMetrics.GLOBAL:
            self._run_derivate(list_of_queries, kind_metrics)
        if kind_metrics == KindMetrics.PER_CLASS:
            for class_name in self.classes:
                self._run_derivate(list_of_queries, kind_metrics, class_name)
        if kind_metrics == KindMetrics.PER_PACKAGE:
            for package_name in self.packages:
                self._run_derivate(list_of_queries, kind_metrics, package_name)

    def _run_derivate(self, list_of_queries: list, kind_metrics: KindMetrics, argument: str = "") -> None:
        """
        Run the list of derivate queries.
        """
        for query in list_of_queries:
            self.set_resuts(kind_metrics, argument)
            result = self.derivate_metrics_generator.run_derivate(
                query['query'], self.results)

            metric_name = self.set_metric_name(
                query['metric'], kind_metrics, argument)
            self.save_metric(metric_name, result, kind_metrics.value)

            self.derivate_metrics_generator.send_result(
                result, kind_metrics.value, metric_name)

    def set_resuts(self, kind_metrics: KindMetrics, argument: str) -> None:
        """
        Set the results dictionary.
        """
        if kind_metrics == KindMetrics.PER_PACKAGE:
            self.results['package'] = argument

    def set_metric_name(self, metric_name: str, kind_metrics: KindMetrics, argument: str) -> str:
        """
        Set the metric name.
        """
        if kind_metrics == KindMetrics.PER_CLASS:
            return argument + '_' + metric_name
        if kind_metrics == KindMetrics.PER_PACKAGE:
            return argument + '_' + metric_name
        return metric_name

    def save_metric(self, metric_name: str, result: int, kind: KindMetrics) -> None:
        """
        Save the metric in the results dictionary.
        """
        if kind == KindMetrics.GLOBAL:
            self.add_global_metric(metric_name, result)
        elif kind == KindMetrics.PER_CLASS:
            self.add_class_metric(metric_name, result)
        else:
            self.add_package_metric(metric_name, result)

    @overrides
    def add_global_metric(self, name: str, value: int) -> None:
        """
        Add a global metric to the API.
        """
        self.results[name] = value

    @overrides
    def add_class_metric(self, name: str, class_name: str, value: int) -> None:
        """
        Add a class metric to the API.
        """
        self.results[class_name + '_' + name] = value

    @overrides
    def add_package_metric(self, name: str, package: str, value: int) -> None:
        """
        Add a package metric to the API.
        """
        self.results[package + '_' + name] = value
