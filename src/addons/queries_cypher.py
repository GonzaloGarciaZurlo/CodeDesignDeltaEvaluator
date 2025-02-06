"""
This module contains functions for handling database queries.
"""
from neo4j import GraphDatabase, Transaction
from overrides import override
import yaml
from src.cdde.result_queries import ResultQueries
from src.cdde.api import CddeAPI
from src.cdde.eval import safe_eval
from src.cdde.result_observer import ResultObserver

TIME_METRICS = ['snapshot-metrics', 'delta-metrics']
KIND_METRICS = ['global', 'per-class', 'per-package']


class QueriesCypher(ResultQueries):
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self, observer: ResultObserver) -> None:
        super().__init__(observer)
        self.uri = "bolt://localhost:7689"
        self.driver = GraphDatabase.driver(
            self.uri, auth=None)
        self.classes: list = []
        self.packages: list = []
        self.queries: dict = {}
        self.derivate_queries: dict = {}
        self.results: dict = {}

    @override
    def resolve_query(self) -> None:
        """
        Resolves all queries.
        """
        self.queries = self._load_queries("src/queries/cypher.yml")
        self.derivate_queries = self._load_queries(
            "src/queries/derivate_metrics.yml")

        self.observer.open_observer()

        self.classes = self.get_all_classes()
        self.get_all_relations()
        self.get_all_packages()

        self.execute_cypher_metrics()
        self.execute_derivate_metrics()

        self.observer.close_observer()

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

    def execute_cypher_metrics(self) -> None:
        """
        Executes all cypher queries.
        """
        for time_metrics in TIME_METRICS:
            for kind_metrics in KIND_METRICS:
                self.execute_queries(time_metrics, kind_metrics)

    def execute_queries(self, time_metrics: str, kind_metrics: str) -> None:
        """
        Execute all queries for a specific time and kind of metrics.
        """
        list_of_queries = self.queries[time_metrics][kind_metrics]
        if list_of_queries is None:
            return None
        if kind_metrics == 'global':
            self.run_cypher(list_of_queries, kind_metrics)
        if kind_metrics == 'per-class':
            for class_name in self.classes:
                self.run_cypher(list_of_queries, kind_metrics, class_name)
        if kind_metrics == 'per-package':
            for package_name in self.packages:
                self.run_cypher(list_of_queries, kind_metrics, package_name)

    def run_cypher(self, list_of_queries: list, kind_metrics: str, argument: str = "") -> None:
        """
        Run the list of queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        params = {}
        for query in list_of_queries:
            params = self.set_params(params, query, argument)

            with self.driver.session() as session:
                result = session.execute_read(
                    lambda tx: tx.run(query['query'], **params).single()[0])
            metric_name = query['metric']

            if argument == "":
                self.observer.on_result_metric_found(
                    result, kind_metrics, metric_name)
                self.results[metric_name] = int(result)
            else:
                self.observer.on_result_metric_found(
                    result, kind_metrics, argument + '_' + metric_name)
                self.results[argument + '_' + metric_name] = int(result)

    def set_params(self, params: dict, query: dict, argument: str) -> dict:
        """
        Set the parameters of the query.
        """
        if "$class_name" in query['query']:
            params["class_name"] = argument
        if "$package_name" in query['query']:
            params["package_name"] = argument
        return params

    def execute_derivate_metrics(self) -> None:
        """
        Executes all derivate queries.
        """
        for time_metrics in TIME_METRICS:
            for kind_metrics in KIND_METRICS:
                self.execute_derivate_queries(time_metrics, kind_metrics)

    def execute_derivate_queries(self, time_metrics: str, kind_metrics: str) -> None:
        """
        Execute all derivate queries for a specific time and kind of metrics.
        """
        list_of_queries = self.derivate_queries[time_metrics][kind_metrics]
        if list_of_queries is None:
            return None
        if kind_metrics == 'global':
            self.run_derivate(list_of_queries, kind_metrics)
        if kind_metrics == 'per-class':
            for class_name in self.classes:
                self.run_derivate(list_of_queries, kind_metrics, class_name)
        if kind_metrics == 'per-package':
            for package_name in self.packages:
                self.run_derivate(list_of_queries, kind_metrics, package_name)

    def run_derivate(self, list_of_queries: list, kind_metrics: str, argument: str = "") -> None:
        """
        Run the list of derivate queries.
        Set the result in the results dictionary.
        Send the result to the observer.
        """
        for query in list_of_queries:

            self.results['package'] = argument

            formula = query['query']
            result = safe_eval(formula, self.results)
            metric_name = query['metric']

            if argument == "":
                self.observer.on_result_metric_found(
                    result, kind_metrics, metric_name)
                self.results[metric_name] = result
            else:
                self.observer.on_result_metric_found(
                    result, kind_metrics, argument + '_' + metric_name)
                self.results[argument + '_' + metric_name] = result

    def get_all_classes(self) -> list:
        """
        Gets all classes in the database.
        """
        with self.driver.session() as session:
            result = session.execute_read(self._get_all_classes)
            self.observer.on_result_data_found(str(result), "classes")
            self.observer.on_result_metric_found(
                len(result), "classes", "total")
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

    def get_all_relations(self) -> None:
        """
        Gets all relations of a class.
        """
        for class_name in self.classes:
            with self.driver.session() as session:
                session.execute_read(self._get_all_relations, class_name)

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

    def get_all_packages(self) -> None:
        """
        Sets all of the packages in the database.
        """
        for class_name in self.classes:
            with self.driver.session() as session:
                session.execute_read(self._get_packages, class_name)

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
