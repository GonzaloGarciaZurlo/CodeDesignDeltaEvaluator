"""
Module for the MetricsAPI class.
In this module we define the API for the metrics used in CodeDesignDeltaEvaluator.
"""
from enum import Enum
from typing import Final
from .expr_evaluator import ExprEvaluator, MetricType
from .metric_result_observer import ResultObserver
from .design_db import DesignDB


class TimeMetrics(Enum):
    """
    Time metrics for queries.
    """
    SNAPSHOT_METRICS = 'snapshot-metrics'
    DELTA_METRICS = 'delta-metrics'


class KindMetrics(Enum):
    """
    Kind of metrics for queries.
    """
    GLOBAL = 'global'
    PER_CLASS = 'per-class'
    PER_PACKAGE = 'per-package'


class MetricsAPI:
    """
    Interface for the metrics API.
    """

    def __init__(self, ) -> None:
        self.__results: dict[str, MetricType] = {}

    def add_metric(self, name: str, value: MetricType) -> None:
        """
        Add a global metric to the API.
        """
        self.__results[name] = value

    def get_metric(self, name: str) -> MetricType:
        """
        Get a metric from the API.
        """
        return self.__results[name]

    def get_metrics_dict(self) -> dict[str, str | float]:
        """
        Get all metrics from the API.
        """
        return self.__results


class MetricsCalculator:
    """
    This class is responsible for calculating the metrics.
    This is the main class of the program.
    """

    def __init__(self, exp_evaluator: ExprEvaluator, design_db: DesignDB,
                 result_observer: ResultObserver, yaml: dict[str, str],
                 results: MetricsAPI) -> None:
        self.exp_eval: Final = exp_evaluator
        self.design_db: Final = design_db
        self.result_observer: Final = result_observer
        self.queries: Final = yaml
        self.results: MetricsAPI = results

    def calc_all_expr(self) -> None:
        """
        Executes all metrics.
        """

        self._get_base_metrics(self.design_db)

        self.set_metrics(self.exp_eval)

    def _get_base_metrics(self, design_db: DesignDB) -> None:
        """ Use this method to get the base queries of DesignDB."""
        # set classes
        self.__set_classes(design_db)
        # set relationships
        self.__set_relationships(design_db)
        # set packages
        self.__set_packages(design_db)

    def __set_classes(self, design_db: DesignDB) -> None:
        """ Set the classes of the design_db."""
        self.classes = design_db.get_all_classes()
        self.result_observer.on_result_data_found(str(self.classes), "classes")
        self.result_observer.on_result_metric_found(len(self.classes),
                                                    "classes", "total")

    def __set_relationships(self, design_db: DesignDB) -> None:
        """ Set the relationships of the design_db."""
        for class_name in self.classes:
            result = design_db.get_all_relations(class_name)
            for record in result:
                self.result_observer.on_result_data_found(
                    str(class_name) + ' --> ' + str(record[1]), str(record[0]))

    def __set_packages(self, design_db: DesignDB) -> None:
        """ Set the packages of the design_db."""
        for class_name in self.classes:
            design_db._set_packages(class_name)

        self.packages = design_db.get_all_packages()
        self.result_observer.on_result_data_found(str(self.packages),
                                                  "packages")

    def set_metrics(self, evaluator: ExprEvaluator) -> None:
        """
        Executes all cypher queries.
        """
        for time_metrics in TimeMetrics:
            for kind_metrics in KindMetrics:
                self.execute_metrics(time_metrics, kind_metrics, evaluator)

    def execute_metrics(self, time_metrics: TimeMetrics,
                        kind_metrics: KindMetrics,
                        evaluator: ExprEvaluator) -> None:
        """
        Execute all queries for a specific time and kind of metrics.
        """
        list_of_queries = self.queries[time_metrics.value][kind_metrics.value]
        if list_of_queries is None:
            return None
        if kind_metrics == KindMetrics.GLOBAL:
            self._run(list_of_queries, kind_metrics, evaluator)
        if kind_metrics == KindMetrics.PER_CLASS:
            for class_name in self.classes:
                self._run(list_of_queries, kind_metrics, evaluator, class_name)
        if kind_metrics == KindMetrics.PER_PACKAGE:
            for package_name in self.packages:
                self._run(list_of_queries, kind_metrics, evaluator,
                          package_name)

    def _run(self,
             list_of_queries: list,
             kind_metrics: KindMetrics,
             evaluator: ExprEvaluator,
             argument: str = "") -> None:
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        for query in list_of_queries:
            params = self.set_params(argument, kind_metrics)
            results_api = self.results.get_metrics_dict()
            result = evaluator.eval(query['query'], params, results_api)

            metric_name = self.set_metric_name(query['metric'], kind_metrics,
                                               argument)
            self.results.add_metric(metric_name, result)

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
            self.results.add_metric('class', argument)
        if kind_metrics == KindMetrics.PER_PACKAGE:
            params["package_name"] = argument
            self.results.add_metric('package', argument)
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
