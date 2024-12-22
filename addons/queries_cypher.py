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
        self.derivate_queries = self._load_queries("queries/derivate_metrics.yml")
        self.observer.open_observer()

        classes = self.get_all_classes()
        self._execute_before_query()
        self._execute_after_query()
        self._execute_general_query()
        class_name = ""
        for class_name in classes:
            self.get_all_relations(class_name)
            self._execute_per_class_query(class_name)

        self._execute_derivate_metrics()
        self.observer.close_observer()

    def _execute_derivate_metrics(self) -> None:
        """
        Executes a query.
        """
        for metric in self.derivate_queries["derivate_metrics"]:
            formula = self.derivate_queries["derivate_metrics"][metric]
            result = safe_eval(formula, self.results)
            self.observer.on_result_metric_found(result, "derivate_metrics", str(metric))

    def _execute_before_query(self) -> None:
        """
        Executes a query.
        """
        for query in self.queries['before-metrics']:
            with self.driver.session() as session:
                result = session.read_transaction(
                    lambda tx: tx.run(self.queries['before-metrics'][query]).single()[0])
            self.results[query] = result
            self.observer.on_result_metric_found(
                result, "before_classes", str(query))

    def _execute_after_query(self) -> None:
        """
        Executes a query.
        """
        for query in self.queries['after-metrics']:
            with self.driver.session() as session:
                result = session.read_transaction(
                    lambda tx: tx.run(self.queries['after-metrics'][query]).single()[0])
            self.results[query] = result
            self.observer.on_result_metric_found(
                result, "after_classes", str(query))

    def _execute_general_query(self) -> None:
        """
        Executes a query.
        """
        for query in self.queries['general-metrics']:
            with self.driver.session() as session:
                result = session.read_transaction(
                    lambda tx: tx.run(self.queries['general-metrics'][query]).single()[0])
            self.results[query] = result
            self.observer.on_result_metric_found(
                result, "class_differences", str(query))

    def _execute_per_class_query(self, class_name: str) -> None:
        """
        Executes a query.
        """
        for query in self.queries['per-class-metrics']:
            with self.driver.session() as session:
                result = session.read_transaction(
                    lambda tx: tx.run(self.queries['per-class-metrics'][query], class_name=class_name).single()[0])
            self.observer.on_result_metric_found(
                result, str(query), class_name)

    def _load_queries(self, file_path: str) -> dict:
        """
        Loads the queries from a yml file.
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
}

def _safe_eval(node, variables, functions):
        if isinstance(node, ast.Constant):
                return node.n
        elif isinstance(node, ast.Name):
                return variables[node.id] # KeyError -> Unsafe variable
        elif isinstance(node, ast.BinOp):
                op = _operations[node.op.__class__] # KeyError -> Unsafe operation
                left = _safe_eval(node.left, variables, functions)
                right = _safe_eval(node.right, variables, functions)
                if isinstance(node.op, ast.Pow):
                        assert right < 100
                return op(left, right)
        elif isinstance(node, ast.Call):
                assert not node.keywords and not node.starargs and not node.kwargs
                assert isinstance(node.func, ast.Name), 'Unsafe function derivation'
                func = functions[node.func.id] # KeyError -> Unsafe function
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
