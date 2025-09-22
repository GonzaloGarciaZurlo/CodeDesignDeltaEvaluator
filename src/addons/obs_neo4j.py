"""
This module handles the creation of a Neo4j database.
"""
from overrides import override
from neo4j import GraphDatabase, Transaction
from src.cdde.addons_api import CddeAPI
from src.cdde.puml_observer import Observer, Modes, ClassKind, Relationship, MethodKind


class Neo4j(Observer):
    """
    Class responsible for creating and initializing a Neo4j database.
    """

    def __init__(self) -> None:
        self.uri = "bolt://localhost:7689"
        self.driver = GraphDatabase.driver(
            self.uri, auth=None)
        self.mode: Modes

    def _create_class(self, tx: Transaction, name: str, kind: ClassKind) -> None:
        """
        Query to create a node with the class name.
        """
        name = self.mode.value + name
        tx.run(
            f"CREATE (p:class {{name: $name, type: $type}})",  # pylint: disable=f-string-without-interpolation
            name=name, type=kind.value)

    def _create_relation(self, tx: Transaction, class1: str, class2:
                         str, relation: Relationship) -> None:
        """
        Query to create a relationship between two nodes.
        If the nodes do not exist, they are created, 
        with the package attribute set to 'library'.
        """
        class1 = self.mode.value + class1
        class2 = self.mode.value + class2
        mode = self.mode.value + '_'
        query = (
            f"MATCH (a:class), (b:class) "
            f"WHERE a.name = $class1 AND b.name = $class2 "
            f"CREATE (a)-[r:{relation.name}] -> (b)"
        )
        query_check_or_create_a = (
            "MERGE (a {name: $class1}) "
            f"ON CREATE SET a.package = ('{mode}' + 'library')"
            "RETURN a"
        )

        query_check_or_create_b = (
            "MERGE (b {name: $class2})"
            f"ON CREATE SET b.package = ('{mode}' + 'library')"
            "RETURN b"
        )
        tx.run(query_check_or_create_a, class1=class1)
        tx.run(query_check_or_create_b, class2=class2)
        tx.run(query, class1=class1, class2=class2)

    def _create_method(self, tx: Transaction, class_name: str,
                       method_name: str, kind: MethodKind) -> None:
        """
        Query to create a node with the method name.
        """
        class_name = self.mode.value + class_name
        method_name = self.mode.value + method_name
        tx.run(
            f"CREATE (p:method {{name: $method_name, visibility: $kind}})",  # pylint: disable=f-string-without-interpolation
            method_name=method_name, kind=kind.value)
        tx.run(
            f"""
            MATCH (a:class), (p:method)
            WHERE p.name = $method_name
            AND a.name = $class_name
            CREATE (a)-[:HAS_METHOD]->(p)
            """, class_name=class_name, method_name=method_name)

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
            session.execute_write(self._create_class,  # type: ignore
                                  class_name, kind)

    @override
    def on_relation_found(self, class1: str, class2: str, relation: Relationship) -> None:
        """
        Create a relationship between two nodes.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_relation,    # type: ignore
                                  class1, class2, relation)

    @override
    def on_package_found(self, package_name: str, classes: list) -> None:
        """
        Set the package name to the classes.
        """
        package_name = self.mode.value + package_name
        with self.driver.session() as session:
            for class_name in classes:
                class_name = self.mode.value + class_name
                query = (
                    "MATCH (a) "
                    "WHERE a.name = $class_name "
                    "SET a.package = $package_name"
                )
                session.run(query, class_name=class_name,
                            package_name=package_name)

    @override
    def on_method_found(self, class_name: str, method_name: str, kind: MethodKind) -> None:
        """
        Create a node with the method name.
        """
        with self.driver.session() as session:
            session.execute_write(self._create_method,  # type: ignore
                                  class_name, method_name, kind)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('Neo4j', Neo4j)
