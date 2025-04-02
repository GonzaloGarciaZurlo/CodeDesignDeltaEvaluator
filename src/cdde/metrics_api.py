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
    def execute_all_metrics(self) -> None:
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
        self.results: dict = {}

    @overrides
    def add_metric(self, name: str, value: int) -> None:
        """
        Add a global metric to the API.
        """
        self.results[name] = value

    @overrides
    def execute_all_metrics(self) -> None:
        """
        Executes all metrics.
        """
        for generator in self.metrics_generators:
            self.queries = generator.get_queries()

            if isinstance(generator, AddonsMetricGenerator):
                self._get_base_metrics(generator)

            self.set_metrics(generator)

    def _get_base_metrics(self, generator: AddonsMetricGenerator) -> None:
        """ Use this method to get the base metrics of a AddonsMetricGenerator."""
        # set classes
        self.__set_classes(generator)
        # set relationships
        self.__set_relationships(generator)
        # set packages
        self.__set_packages(generator)

    def __set_classes(self, generator: AddonsMetricGenerator) -> None:
        """ Set the classes of the generator."""
        self.classes = generator.get_all_classes()
        self.result_observer.on_result_data_found(str(self.classes), "classes")
        self.result_observer.on_result_metric_found(len(self.classes),
                                                    "classes", "total")

    def __set_relationships(self, generator: AddonsMetricGenerator) -> None:
        """ Set the relationships of the generator."""
        for class_name in self.classes:
            result = generator.get_all_relations(class_name)
            for record in result:
                self.result_observer.on_result_data_found(
                    str(class_name) + ' --> ' + str(record[1]), str(record[0]))

    def __set_packages(self, generator: AddonsMetricGenerator) -> None:
        """ Set the packages of the generator."""
        for class_name in self.classes:
            generator.set_packages(class_name)

        self.packages = generator.get_all_packages()
        self.result_observer.on_result_data_found(str(self.packages),
                                                  "packages")

    def set_metrics(self, generator: MetricGenerator) -> None:
        """
        Executes all cypher queries.
        """
        for time_metrics in TimeMetrics:
            for kind_metrics in KindMetrics:
                self.execute_metrics(time_metrics, kind_metrics, generator)

    def execute_metrics(self, time_metrics: TimeMetrics,
                        kind_metrics: KindMetrics,
                        generator: MetricGenerator) -> None:
        """
        Execute all queries for a specific time and kind of metrics.
        """
        list_of_queries = self.queries[time_metrics.value][kind_metrics.value]
        if list_of_queries is None:
            return None
        if kind_metrics == KindMetrics.GLOBAL:
            self._run(list_of_queries, kind_metrics, generator)
        if kind_metrics == KindMetrics.PER_CLASS:
            for class_name in self.classes:
                self._run(list_of_queries, kind_metrics, generator, class_name)
        if kind_metrics == KindMetrics.PER_PACKAGE:
            for package_name in self.packages:
                self._run(list_of_queries, kind_metrics, generator,
                          package_name)

    def _run(self,
             list_of_queries: list,
             kind_metrics: KindMetrics,
             generator: MetricGenerator,
             argument: str = "") -> None:
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        for query in list_of_queries:
            params = self.set_params(argument, kind_metrics)
            result = generator.run_metric(query['query'], params, self.results)

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
            self.results['class'] = argument
        if kind_metrics == KindMetrics.PER_PACKAGE:
            params["package_name"] = argument
            self.results['package'] = argument
        return params

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
