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
            self.uri, auth=("neo4j", "holacomoestas"))

    def _create_class(self, tx: Transaction, name: str) -> None:
        """
        Query to create a node with the class name.
        """
        tx.run("CREATE (p:Class {name: $name})", name=name)

    def _create_relation(self, tx: Transaction, class1: str, class2: str, relation: str) -> None:
        """
        Query to create a relationship between two nodes.
        """
        query = (
            f"MATCH (a:Class), (b:Class) "
            f"WHERE a.name = $class1 AND b.name = $class2 "
            f"CREATE (a)-[r:{relation}] -> (b)"
        )
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
        pass

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """
        self.close()

    @override
    def on_class_found(self, class_name: str, kind: str) -> None:
        """
        Create a node with the class name.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_class, class_name)

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        """
        Create a relationship between two nodes.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_relation,
                                  class1, class2, relation)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('neo4j', Neo4j)
