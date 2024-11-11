"""
This module contains functions for handling database queries.
"""
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

    @override
    def resolve_query(self) -> None:
        """
        Resolves all queries.
        """
        self.queries = self._load_queries("queries/cypher.yml")
        class_name = ""
        self.observer.open_observer()
        classes = self.get_all_classes()
        self.observer.on_result_metric_found(len(classes), "Nclasses", "total")
        self.get_diff_classes()
        for class_name in classes:
            self.get_class_coupling(class_name)
            self.get_dependency(class_name)
            self.get_all_relations(class_name)
        self.observer.close_observer()

    def _load_queries(self, file_path: str) -> dict:
        queries_dict = {}
        with open(file_path, 'r', encoding="utf-8") as file:
            data = yaml.safe_load(file)

        for section in ['per-class-metrics', 'general-metrics']:
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
        return result

    def _get_all_classes(self, tx: Transaction) -> list:
        """
        Helper function to get all classes in the database.
        """
        query = self.queries['general-metrics']['all_classes']
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
        query = self.queries['general-metrics']['all_relations']
        result1 = tx.run(query, class_name=class_name)
        for record in result1:
            self.observer.on_result_data_found(
                str(class_name)+' --> '+str(record['dependent']), str(record["relation"]))

    def get_class_coupling(self, class_name: str) -> None:
        """
        Gets the coupling of a class.
        """
        with self.driver.session() as session:
            session.read_transaction(self._calculate_coupling, class_name)

    def _calculate_coupling(self, tx: Transaction, class_name: str) -> None:
        """
        Calculates the efferent and afferent coupling of a class or abstract class.
        """
        self._calculate_afferent_coupling(tx, class_name)
        self._calculate_efferent_coupling(tx, class_name)

    def _calculate_efferent_coupling(self, tx: Transaction, class_name: str) -> None:
        """
        Calculates the efferent coupling of a class or abstract class.
        """
        query = self.queries['per-class-metrics']['efferent_count']
        result = tx.run(query, class_name=class_name).single()
        self.observer.on_result_metric_found(
            str(result["metric"]), "efferent_coupling", class_name)

    def _calculate_afferent_coupling(self, tx: Transaction, class_name: str) -> int:
        """
        Calculates the afferent coupling of a class or abstract class.
        """
        query = self.queries['per-class-metrics']['afferent_count']
        result = tx.run(query, class_name=class_name).single()
        self.observer.on_result_metric_found(
            str(result["metric"]), "affernt_coupling", class_name)

    def get_dependency(self, class_name: str) -> None:
        """
        Gets the number of concrete and abstract classes on which a class depends..
        """
        with self.driver.session() as session:
            session.read_transaction(self._calculate_dependency, class_name)

    def _calculate_dependency(self, tx: Transaction, class_name: str) -> None:
        """
        Calculates the number of concrete and abstract classes on which a class depends.
        """
        self._calculate_dependency_concrete(tx, class_name)
        self._calculate_dependency_abstract(tx, class_name)

    def _calculate_dependency_abstract(self, tx: Transaction, class_name: str) -> None:
        """
        Calculates the number of abstract classes on which a class depends.
        """
        query = self.queries['per-class-metrics']['abstracts_deps_count']
        result = tx.run(query, class_name=class_name).single()
        self.observer.on_result_metric_found(
            result["metric"], "abstract_dependency", class_name)

    def _calculate_dependency_concrete(self, tx: Transaction, class_name: str) -> None:
        """
        Calculates the number of concrete classes on which a class depends.
        """
        query = self.queries['per-class-metrics']['concrete_deps_count']
        result = tx.run(query, class_name=class_name).single()
        self.observer.on_result_metric_found(
            result["metric"], "concrete_dependency", class_name)

    def get_diff_classes(self) -> None:
        """
        Gets the difference between the classes in the before and after state.
        """
        with self.driver.session() as session:
            session.read_transaction(self._get_delete_classes)
            session.read_transaction(self._get_add_classes)

    def _get_delete_classes(self, tx: Transaction) -> None:
        """
        Get the diference between the classes in the before and after state.
        """
        query = self.queries['general-metrics']['delete_classes']
        result = tx.run(query).single()
        if result is not None:
            self.observer.on_result_data_found(
                result["deleted_nodes"], "deleted_classes")
            self.observer.on_result_metric_found(
                len(result["deleted_nodes"]), "N_deleted_classes", "total")

    def _get_add_classes(self, tx: Transaction) -> None:
        """
        Get the diference between the classes in the before and after state.
        """
        query = self.queries['general-metrics']['add_classes']
        result = tx.run(query).single()
        if result is not None:
            self.observer.on_result_data_found(
                result["added_nodes"], "added_classes")
            self.observer.on_result_metric_found(
                len(result["added_nodes"]), "N_added_classes", "total")


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_result_queries('cypher', QueriesCypher)
