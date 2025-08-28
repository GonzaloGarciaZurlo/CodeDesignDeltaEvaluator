"""
This module is responsible for calculating the metrics.
It handles the execution of queries and the storage of results.
It also manages the communication with the observer.
It is the main class of the program.
"""
from enum import StrEnum
from typing import Final
from .expr_evaluator import ExprEvaluator, MetricType
from .metric_result_observer import ResultObserver
from .design_db import DesignDB


class TimeMetrics(StrEnum):
    """
    Time metrics for queries.
    """
    SNAPSHOT_METRICS = 'snapshot-metrics'
    DELTA_METRICS = 'delta-metrics'


class TypeMetrics(StrEnum):
    """
    Kind of metrics for queries.
    """
    GLOBAL = 'global'
    PER_CLASS = 'per-class'
    PER_PACKAGE = 'per-package'


MetricsRepo = dict[str, MetricType]


class MetricsRepository:
    """
    Handles the metrics repository.
    This class is responsible for storing the metrics.
    """

    def __init__(self, ) -> None:
        self.__results: MetricsRepo = {}

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
                 results: MetricsRepository) -> None:
        self.exp_eval: Final = exp_evaluator
        self.design_db: Final = design_db
        self.result_observer: Final = result_observer
        self.queries: Final = yaml
        self.results: MetricsRepository = results
        self.classes = []
        self.packages = []

    def calc_all_expr(self) -> None:
        """
        Executes all metrics.
        """
        self.result_observer.open_observer()
        self._get_base_metrics(self.design_db)
        self._set_metrics(self.exp_eval)
        self.result_observer.close_observer()

    def _get_base_metrics(self, design_db: DesignDB) -> None:
        """ Use this method to get the base queries of DesignDB."""
        # set classes
        self.__get_classes(design_db)
        # set relationships
        #self.__get_relationships(design_db)
        # set packages
        self.__get_packages(design_db)

    def __get_classes(self, design_db: DesignDB) -> None:
        """ Set the classes of the design_db."""
        self.classes = design_db.get_all_classes()
        #self.result_observer.on_result_data_found(str(self.classes), "classes")
        #self.result_observer.on_result_metric_found(len(self.classes),
        #                                            "classes", "total")

    def __get_relationships(self, design_db: DesignDB) -> None:
        """ Set the relationships of the design_db."""
        for class_name in self.classes:
            result = design_db.get_all_relations(class_name)
            for record in result:
                self.result_observer.on_result_data_found(
                    str(class_name) + ' --> ' + str(record[1]), str(record[0]))

    def __get_packages(self, design_db: DesignDB) -> None:
        """ Set the packages of the design_db."""
        for class_name in self.classes:
            design_db.set_packages(class_name)

        self.packages = design_db.get_all_packages()
        #self.result_observer.on_result_data_found(str(self.packages),
        #                                          "packages")

    def _set_metrics(self, evaluator: ExprEvaluator) -> None:
        """
        Traverse the queries and execute them.
        """
        for time_metrics in TimeMetrics:
            for type_metrics in TypeMetrics:
                self._calc_metrics(time_metrics, type_metrics, evaluator)

    def _calc_metrics(self, time_metrics: TimeMetrics,
                      type_metrics: TypeMetrics,
                      evaluator: ExprEvaluator) -> None:
        """
        Calculate the metric, depending on the time and type of metric.
        """
        list_of_queries = self.queries[time_metrics.value][type_metrics.value]
        if list_of_queries is None:
            return None
        if type_metrics == TypeMetrics.GLOBAL:
            self._run(list_of_queries, type_metrics, evaluator)
        if type_metrics == TypeMetrics.PER_CLASS:
            for class_name in self.classes:
                self._run(list_of_queries, type_metrics, evaluator, class_name)
        if type_metrics == TypeMetrics.PER_PACKAGE:
            for package_name in self.packages:
                self._run(list_of_queries, type_metrics, evaluator,
                          package_name)

    def _run(self,
             list_of_queries: list,
             type_metrics: TypeMetrics,
             evaluator: ExprEvaluator,
             argument: str = "") -> None:
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """

        for query in list_of_queries:
            params = self.__set_params(argument, type_metrics)
            results_api = self.results.get_metrics_dict()
            result = evaluator.eval(query['query'], params, results_api)

            metric_name = self.__set_metric_name(query['metric'], type_metrics,
                                                 argument)
            self.results.add_metric(metric_name, result)

            # Send the result to the observer
            self.result_observer.on_result_metric_found(
                result, type_metrics.value, metric_name)

    def __set_params(self, argument: str, type_metrics: TypeMetrics) -> dict:
        """
        Set the parameters of the query.
        """
        params = {}
        if type_metrics == TypeMetrics.PER_CLASS:
            params["class_name"] = argument
            self.results.add_metric('class', argument)
        if type_metrics == TypeMetrics.PER_PACKAGE:
            params["package_name"] = argument
            self.results.add_metric('package', argument)
        return params

    def __set_metric_name(self, metric_name: str, type_metrics: TypeMetrics,
                          argument: str) -> str:
        """
        Set the metric name.
        """
        if type_metrics == TypeMetrics.PER_CLASS:
            return argument + '___SEP___' + metric_name
        if type_metrics == TypeMetrics.PER_PACKAGE:
            return argument + '___SEP___' + metric_name
        return metric_name
