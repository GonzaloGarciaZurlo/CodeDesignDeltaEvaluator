"""
This module handles the creation of a Neo4j database.
"""
from overrides import override
from neo4j import GraphDatabase, Transaction
from api import CddeAPI
from puml_observer import Observer


class Neo4j(Observer):
    """
    Class responsible for creating and initializing a Neo4j database.
    """

    def __init__(self) -> None:
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(
            self.uri, auth=None)

    def _create_class(self, tx: Transaction, name: str, kind: str, label: str) -> None:
        """
        Query to create a node with the class name.
        """
        name = label + name
        tx.run(f"CREATE (p:{kind} {{name: $name}})", name=name)

    def _create_relation(self, tx: Transaction, class1: str, class2:
                         str, relation: str, label: str) -> None:
        """
        Query to create a relationship between two nodes.
        """
        class1 = label + class1
        class2 = label + class2
        query = (
            f"MATCH (a), (b) "
            f"WHERE a.name = $class1 AND b.name = $class2 "
            f"CREATE (a)-[r:{relation}] -> (b)"
        )
        query_check_or_create_a = (
            "MERGE (a {name: $class1}) "
            "SET a.package = 'library'"
            "RETURN a"
        )

        query_check_or_create_b = (
            "MERGE (b {name: $class2}) "
            "SET b.package = 'library'"
            "RETURN b"
        )
        tx.run(query_check_or_create_a, class1=class1)
        tx.run(query_check_or_create_b, class2=class2)
        tx.run(query, class1=class1, class2=class2)

    def delete_all(self) -> None:
        """
        Delete all nodes and relationships in the database.
        """
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def close(self):
        """
        Close the connection to the database.
        """
        self.driver.close()

    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened.
        """

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """
        self.close()

    @override
    def on_class_found(self, class_name: str, kind: str, label: str) -> None:
        """
        Create a node with the class name.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_class, class_name, kind, label)

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str, label: str) -> None:
        """
        Create a relationship between two nodes.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_relation,
                                  class1, class2, relation, label)

    @override
    def on_package_found(self, package_name: str, classes: list,  label: str) -> None:
        """
        Set the package name to the classes.
        """
        package_name = label + '_' + package_name
        with self.driver.session() as session:
            for class_name in classes:
                class_name = label + class_name
                query = (
                    "MATCH (a) "
                    "WHERE a.name = $class_name "
                    "SET a.package = $package_name"
                )
                session.run(query, class_name=class_name,
                            package_name=package_name)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('neo4j', Neo4j)
