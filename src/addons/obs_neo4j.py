"""
This module handles the creation of a Neo4j database.
"""
from overrides import override
from neo4j import GraphDatabase, Transaction
from src.CddE.api import CddeAPI
from src.CddE.puml_observer import Observer, Modes, ClassKind, Relationship


class Neo4j(Observer):
    """
    Class responsible for creating and initializing a Neo4j database.
    """

    def __init__(self) -> None:
        self.uri = "bolt://localhost:7689"
        self.driver = GraphDatabase.driver(
            self.uri, auth=None)
        self.mode = None

    def _create_class(self, tx: Transaction, name: str, kind: ClassKind) -> None:
        """
        Query to create a node with the class name.
        """
        name = self.mode + name
        tx.run(f"CREATE (p:{kind.value} {{name: $name}})", name=name)

    def _create_relation(self, tx: Transaction, class1: str, class2:
                         str, relation: Relationship) -> None:
        """
        Query to create a relationship between two nodes.
        If the nodes do not exist, they are created, 
        with the package attribute set to 'library'.
        """
        class1 = self.mode + class1
        class2 = self.mode + class2
        query = (
            f"MATCH (a), (b) "
            f"WHERE a.name = $class1 AND b.name = $class2 "
            f"CREATE (a)-[r:{relation.name}] -> (b)"
        )
        query_check_or_create_a = (
            "MERGE (a {name: $class1}) "
            "ON CREATE SET a.package = 'library'"
            "RETURN a"
        )

        query_check_or_create_b = (
            "MERGE (b {name: $class2}) "
            "ON CREATE SET b.package = 'library'"
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
    def set_mode(self, mode: Modes) -> None:
        """
        Set the mode of the observer.
        """
        self.mode = mode

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
    def on_class_found(self, class_name: str, kind: ClassKind) -> None:
        """
        Create a node with the class name.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_class, class_name, kind)

    @override
    def on_relation_found(self, class1: str, class2: str, relation: Relationship) -> None:
        """
        Create a relationship between two nodes.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_relation,
                                  class1, class2, relation)

    @override
    def on_package_found(self, package_name: str, classes: list) -> None:
        """
        Set the package name to the classes.
        """
        package_name = self.mode.value + '_' + package_name
        with self.driver.session() as session:
            for class_name in classes:
                class_name = self.mode + class_name
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
    api.register_puml_observer('Neo4j', Neo4j)
