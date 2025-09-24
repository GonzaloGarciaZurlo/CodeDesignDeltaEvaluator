""" Basic queries to interact with the Neo4j database. """
from overrides import override
from neo4j import Transaction, GraphDatabase
from src.cdde.design_db import DesignDB, RelationshipType
from src.cdde.addons_api import CddeAPI


class DesignDBNeo4j(DesignDB):
    """
    Class to interact with the Neo4j database.
    """

    def __init__(self) -> None:
        self.uri = self._get_uri()
        self.driver = GraphDatabase.driver(self.uri, auth=None)
        self.path: str = "src/queries/cypher.yml"
        self.packages: list[str] = []

    def _get_uri(self) -> str:
        """
        Get the URI of the Neo4j database in the uri.txt file.
        """
        try:
            with open("uri.txt", 'r', encoding="utf-8") as file:
                return file.read().strip()
        except:
            return "bolt://localhost:7689"

    @override
    def get_all_classes(self) -> list[str]:
        """
        Gets all classes in the database.
        """
        with self.driver.session() as session:
            result = session.execute_read(
                self._get_all_classes_)  # type: ignore
        return result

    @override
    def get_class_per_package(self, package_name: str) -> list[str]:
        """
        Gets all classes in a package.
        """
        with self.driver.session() as session:
            return session.execute_read(
                self._get_class_per_package_,  # type: ignore
                package_name)

    @override
    def get_all_relations(self, class_name: str) -> list[RelationshipType]:
        """
        Gets all relations of a class.
        """
        with self.driver.session() as session:
            return session.execute_read(
                self._get_all_relations_,  # type: ignore
                class_name)

    @override
    def get_methods_per_class(self, class_name: str) -> list[str]:
        return []

    def _get_class_per_package_(self, tx: Transaction,
                                package_name: str) -> list:
        """
        Helper function to get all classes in a package.
        """
        query = """
                MATCH (c:class {package: $package_name}) RETURN c.name AS name
                """
        result = tx.run(query, package_name=package_name)
        return [record["name"] for record in result]

    def _get_all_classes_(self, tx: Transaction) -> list:
        """
        Helper function to get all classes in the database.
        """
        query = """
                MATCH (c:class) RETURN c.name AS name
                """
        result = tx.run(query)
        return [record["name"] for record in result]

    def _get_all_relations_(self, tx: Transaction,
                            class_name: str) -> list[tuple]:
        """
        Helper function to get all relations of a class.
        """
        query = """
                MATCH (c:class {name: $class_name})-[r]->(dependent)
                RETURN type(r) AS relation, dependent.name AS dependent
                """
        result = tx.run(query, class_name=class_name)
        r = []
        for record in result:
            r.append((record["relation"], record["dependent"]))
        return r

    @override
    def set_packages(self, class_name: str) -> None:
        """
        Sets all of the packages in the database.
        """
        with self.driver.session() as session:
            result = session.execute_write(
                self._set_packages_,  # type: ignore
                class_name)
        if result and result not in self.packages:
            self.packages.append(result)

    def _set_packages_(self, tx: Transaction, class_name: str) -> None:
        """
        Helper function to get all of the packages in the database.
        """
        query = """
                MATCH (c:class {name: $class_name})
                RETURN c.package AS package
                """
        return tx.run(query, class_name=class_name).single()[0]  # type: ignore

    @override
    def get_all_packages(self) -> list[str]:
        """
        Gets all packages in the database.
        """
        return self.packages


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_design_db('Neo4j', DesignDBNeo4j)
