"""
Module for the MetricsAPI class.
In this module we define the API for the metrics used in CodeDesignDeltaEvaluator.
"""
from abc import ABC, abstractmethod
from overrides import overrides
import yaml
from enum import Enum
from .metric_generator import AddonsMetricGenerator, MetricGenerator
from .metric_result_observer import ResultObserver


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
    def add_metric(self, name: str, value: int) -> None:
        """
        Add a global metric to the API.
        """

    @abstractmethod
    def execute_all_metrics(self,
                            list_generators: list[MetricGenerator]) -> None:
        """
        Executes all metrics.
        """


class MetricsCalculator(MetricsAPI):
    """
    This class implements the MetricsAPI interface.
    """

    def __init__(self, metric_generators: list[MetricGenerator],
                 result_obs: ResultObserver) -> None:
        self.metrics_generators = metric_generators
        self.result_observer = result_obs
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
        for generator in self.metrics_generators:
            self.queries = self._load_queries(generator.get_file_path())

            if isinstance(generator, AddonsMetricGenerator):
                self.classes = generator.get_all_classes()
                self.result_observer.on_result_data_found(
                    str(self.classes), "classes")
                self.result_observer.on_result_metric_found(
                    len(self.classes), "classes", "total")

                for class_name in self.classes:
                    result = generator.get_all_relations(class_name)
                    for record in result:
                        self.result_observer.on_result_data_found(
                            str(class_name) + ' --> ' + str(record[0]),
                            str(record[1]))

                for class_name in self.classes:
                    generator.set_packages(class_name)

                self.packages = generator.get_all_packages()
                self.result_observer.on_result_data_found(
                    str(self.packages), "packages")

            self.set_metrics(generator)

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
                self.execute_metrics(time_metrics, kind_metrics,
                                     metric_Generator)

    def execute_metrics(self, time_metrics: TimeMetrics,
                        kind_metrics: KindMetrics,
                        metric_generator: MetricGenerator) -> None:
        """
        Execute all queries for a specific time and kind of metrics.
        """
        list_of_queries = self.queries[time_metrics.value][kind_metrics.value]
        if list_of_queries is None:
            return None
        if kind_metrics == KindMetrics.GLOBAL:
            self._run(list_of_queries, kind_metrics, metric_generator)
        if kind_metrics == KindMetrics.PER_CLASS:
            for class_name in self.classes:
                self._run(list_of_queries, kind_metrics, metric_generator,
                          class_name)
        if kind_metrics == KindMetrics.PER_PACKAGE:
            for package_name in self.packages:
                self._run(list_of_queries, kind_metrics, metric_generator,
                          package_name)

    def _run(self,
             list_of_queries: list,
             kind_metrics: KindMetrics,
             metric_generator: MetricGenerator,
             argument: str = "") -> None:
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        for query in list_of_queries:
            if isinstance(metric_generator, AddonsMetricGenerator):
                params = self.set_params(argument, kind_metrics)
                result = metric_generator.run_metrics(query['query'], params)
            else:
                self.set_resuts(kind_metrics, argument)
                result = metric_generator.run_metrics(query['query'],
                                                      self.results)

            metric_name = self.set_metric_name(query['metric'], kind_metrics,
                                               argument)
            self.add_metric(metric_name, result)

            # Send the result to the observer
            self.result_observer.on_result_metric_found(
                result, kind_metrics.value, metric_name)

    def set_params(self, argument: str, kind_metrics: KindMetrics) -> dict:
        """
        Set the parameters of the query.
        """
        params = {}
        if kind_metrics == KindMetrics.PER_CLASS:
            params["class_name"] = argument
        if kind_metrics == KindMetrics.PER_PACKAGE:
            params["package_name"] = argument
        return params

    def set_resuts(self, kind_metrics: KindMetrics, argument: str) -> None:
        """
        Set the results dictionary.
        """
        if kind_metrics == KindMetrics.PER_PACKAGE:
            self.results['package'] = argument

    def set_metric_name(self, metric_name: str, kind_metrics: KindMetrics,
                        argument: str) -> str:
        """
        Set the metric name.
        """
        if kind_metrics == KindMetrics.PER_CLASS:
            return argument + '_' + metric_name
        if kind_metrics == KindMetrics.PER_PACKAGE:
            return argument + '_' + metric_name
        return metric_name

    @overrides
    def add_metric(self, name: str, value: int) -> None:
        """
        Add a global metric to the API.
        """
        self.results[name] = value

