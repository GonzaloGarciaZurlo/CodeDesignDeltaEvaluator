"""
This module contains functions for handling database queries.
"""
import ast
import operator
from neo4j import GraphDatabase, Transaction
from overrides import override
from result_queries import ResultQueries
from api import CddeAPI
from result_observer import ResultObserver
import yaml

QUERIES_WITHOUT_PARAMETERS = [
    'before-metrics', 'after-metrics', 'general-metrics']
QUERIES_WITH_ONE_PARAMETER = ['per-class-metrics']
DERIVATE_METRICS = ['derivate_metrics']


class QueriesCypher(ResultQueries):
    """
    This class is responsible for calculating the coupling of a class.
    """

    def __init__(self, observer: ResultObserver) -> None:
        super().__init__(observer)
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(
            self.uri, auth=None)
        self.queries = {}
        self.derivate_queries = {}
        self.results = {}

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
            self.metrics_with_one_parameter(class_name)

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

    def metrics_with_one_parameter(self, parameter: str) -> None:
        """
        Iterates through all types of queries with one parameter
        """
        for kind in QUERIES_WITH_ONE_PARAMETER:
            for query in self.queries[kind]:
                self._execute_metrics_with_one_parameter(
                    kind, query, parameter)

    def _execute_metrics_with_one_parameter(self, kind: str, query: str, parameter: str) -> None:
        """
        Executes all metrics with one parameter.
        """
        with self.driver.session() as session:
            result = session.read_transaction(
                lambda tx: tx.run(self.queries[kind][query], class_name=parameter).single()[0])
            self.results[query] = result
            self.observer.on_result_metric_found(
                result, query, parameter)

    def derivate_metrics(self) -> None:
        """
        Iterates through all types of derivate metrics
        """
        for kind in DERIVATE_METRICS:
            self._execute_derivate_metrics(kind)

    def _execute_derivate_metrics(self, kind: str) -> None:
        """
        Executes all derivate metrics.
        """
        for metric in self.derivate_queries[kind]:
            formula = self.derivate_queries[kind][metric]
            result = safe_eval(formula, self.results)
            self.observer.on_result_metric_found(
                result, kind, metric)

    def get_all_classes(self) -> list:
        """
        Gets all classes in the database.
        """
        with self.driver.session() as session:
            result = session.read_transaction(self._get_all_classes)
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


_operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    'abs': abs
}


def _safe_eval(node, variables, functions):
    if isinstance(node, ast.Constant):
        return node.n
    elif isinstance(node, ast.Name):
        return variables[node.id]  # KeyError -> Unsafe variable
    elif isinstance(node, ast.BinOp):
        op = _operations[node.op.__class__]  # KeyError -> Unsafe operation
        left = _safe_eval(node.left, variables, functions)
        right = _safe_eval(node.right, variables, functions)
        if isinstance(node.op, ast.Pow):
            assert right < 100
        return op(left, right)
    elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'abs':
        # Manejar la función abs
        arg = _safe_eval(node.args[0], variables, functions)
        return abs(arg)
    elif isinstance(node, ast.Call):
        assert not node.keywords and not node.starargs and not node.kwargs
        assert isinstance(node.func, ast.Name), 'Unsafe function derivation'
        func = functions[node.func.id]  # KeyError -> Unsafe function
        args = [_safe_eval(arg, variables, functions) for arg in node.args]
        return func(*args)

    assert False, 'Unsafe operation'


def safe_eval(expr, variables={}, functions={}):
    node = ast.parse(expr, '<string>', 'eval').body
    return _safe_eval(node, variables, functions)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_queries('cypher', QueriesCypher)
