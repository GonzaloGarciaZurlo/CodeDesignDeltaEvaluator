"""
This module contains functions for handling database queries.
"""
from neo4j import GraphDatabase, Transaction
from overrides import override
from result_queries import ResultQueries
from api import CddeAPI
from eval import safe_eval
from result_observer import ResultObserver
import yaml

QUERIES_WITHOUT_PARAMETERS = [
    'before-metrics', 'after-metrics', 'general-metrics']
PER_CLASS_METRICS = ['per-class-metrics']
PER_PACKAGE_METRICS = ['per-package-metrics']
DERIVATE_METRICS = ['derivate_metrics', 'per-package-derivate-metrics']


class QueriesCypher(ResultQueries):
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self, observer: ResultObserver) -> None:
        super().__init__(observer)
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(
            self.uri, auth=None)
        self.packages: list = []
        self.queries: dict = {}
        self.derivate_queries: dict = {}
        self.results: dict = {}

    @override
    def resolve_query(self) -> None:
        """
        Resolves all queries.
        """
        self.queries = self._load_queries("queries/cypher.yml")
        self.derivate_queries = self._load_queries(
            "queries/derivate_metrics.yml")
        self.observer.open_observer()

        classes = self.get_all_classes()
        self.metrics_without_parameters()

        for class_name in classes:
            self.get_all_relations(class_name)
            self.metrics_per_class(class_name)
            self._set_packages(class_name)

        for package in self.packages:
            self.metrics_per_package(package)
        self.derivate_metrics()
        self.observer.close_observer()

    def _load_queries(self, file_path: str) -> dict:
        """
        Loads the queries from a yml file.
        Each section of the yml file must have the form:
        - metric: ...
          query: ...
        """
        queries_dict = {}
        with open(file_path, 'r', encoding="utf-8") as file:
            data = yaml.safe_load(file)

        types_of_metrics = data.keys()

        for section in types_of_metrics:
            if section in data:
                queries_dict[section] = {
                    metric_entry['metric']: metric_entry['query']
                    for metric_entry in data[section]
                }
        return queries_dict

    def metrics_without_parameters(self) -> None:
        """
        Iterates through all types of queries without parameters
        """
        for kind in QUERIES_WITHOUT_PARAMETERS:
            for query in self.queries[kind]:
                self._execute_metrics_without_parameters(kind, query)

    def _execute_metrics_without_parameters(self, kind: str, query: str) -> None:
        """
        Executes alls metrics without parameters.
        """
        with self.driver.session() as session:
            result = session.read_transaction(
                lambda tx: tx.run(self.queries[kind][query]).single()[0])
            self.results[query] = result
            self.observer.on_result_metric_found(
                result, kind, query)

    def metrics_per_class(self, parameter: str) -> None:
        """
        Iterates through all types of queries with one parameter (class name)
        """
        for kind in PER_CLASS_METRICS:
            for query in self.queries[kind]:
                self._execute_metrics_per_class(
                    kind, query, parameter)

    def _execute_metrics_per_class(self, kind: str, query: str, parameter: str) -> None:
        """
        Executes all metrics for a class.
        """
        with self.driver.session() as session:
            result = session.read_transaction(
                lambda tx: tx.run(self.queries[kind][query], class_name=parameter).single()[0])
            self.results[query] = result
            self.observer.on_result_metric_found(
                result, kind, parameter + '_' + query)

    def metrics_per_package(self, parameter: str) -> None:
        """
        Iterates through all types of queries with one parameter (package name)
        """
        for kind in PER_PACKAGE_METRICS:
            for query in self.queries[kind]:
                self._execute_metrics_per_package(
                    kind, query, parameter)

    def _execute_metrics_per_package(self, kind: str, query: str, parameter: str) -> None:
        """
        Executes all metrics for a package.
        """
        with self.driver.session() as session:
            result = session.read_transaction(
                lambda tx: tx.run(self.queries[kind][query], package_name=parameter).single()[0])

            self.results[parameter + query] = result
            self.observer.on_result_metric_found(
                result, kind, parameter + '_' + query)

    def derivate_metrics(self) -> None:
        """
        Iterates through all types of derivate metrics
        """
        for kind in DERIVATE_METRICS:
            if kind == 'derivate_metrics':
                self._execute_derivate_metrics(kind)
            elif kind == 'per-package-derivate-metrics':
                for package in self.packages:
                    self.per_packages_derivate_metrics(kind, package)

    def _execute_derivate_metrics(self, kind: str) -> None:
        """
        Executes all derivate metrics.
        """
        for metric in self.derivate_queries[kind]:
            formula = self.derivate_queries[kind][metric]
            result = safe_eval(formula, self.results)
            self.results[metric] = result
            self.observer.on_result_metric_found(
                result, kind, metric)

    def per_packages_derivate_metrics(self, kind: str, package: str) -> None:
        """
        Executes all derivate metrics for a package.
        """
        for metric in self.derivate_queries[kind]:
            formula = self.derivate_queries[kind][metric]
            for package in self.packages:
                self.results['package'] = package
                if 'before' in metric and 'before' in package:
                    result = safe_eval(formula, self.results)
                    self.observer.on_result_metric_found(
                        result, kind, package + '_' + metric)
                elif 'after' in metric and 'after' in package:
                    result = safe_eval(formula, self.results)
                    self.observer.on_result_metric_found(
                        result, kind, package + '_' + metric)
                elif 'after' not in metric and 'before' not in metric:
                    result = safe_eval(formula, self.results)
                    self.observer.on_result_metric_found(
                        result, kind, package + '_' + metric)
                else:
                    result = 0
                self.results[package + metric] = result

    def get_all_classes(self) -> list:
        """
        Gets all classes in the database.
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_classes)
            self.observer.on_result_data_found(str(result), "classes")
            self.observer.on_result_metric_found(
                str(len(result)), "classes", "total")
        return result

    def _get_all_classes(self, tx: Transaction) -> list:
        """
        Helper function to get all classes in the database.
        """
        query = """
                MATCH (c) RETURN c.name AS name
                """
        result = tx.run(query)
        return [record["name"] for record in result]

    def get_all_relations(self, class_name: str) -> None:
        """
        Gets all relations of a class.
        """
        with self.driver.session() as session:
            session.read_transaction(self._get_all_relations, class_name)

    def _get_all_relations(self, tx: Transaction, class_name: str) -> None:
        """
        Helper function to get all relations of a class.
        """
        query = """
                MATCH (c {name: $class_name})-[r]->(dependent)
                RETURN type(r) AS relation, dependent.name AS dependent
                """
        result = tx.run(query, class_name=class_name)
        for record in result:
            self.observer.on_result_data_found(
                str(class_name)+' --> '+str(record['dependent']), str(record["relation"]))

    def _set_packages(self, class_name: str) -> None:
        """
        Sets all of the packages in the database.
        """
        with self.driver.session() as session:
            session.read_transaction(self._get_packages, class_name)

    def _get_packages(self, tx: Transaction, class_name: str) -> None:
        """
        Helper function to get all of the packages in the database.
        """
        query = """
                MATCH (c {name: $class_name})
                RETURN c.package AS package
                """
        result = tx.run(query, class_name=class_name).single()[0]
        if result not in self.packages:
            self.packages.append(result)
        if self.packages == [None]:
            self.packages = []


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_queries('cypher', QueriesCypher)
