from parser.puml_observer import Observer
from neo4j import GraphDatabase
from overrides import override


class Neoj4(Observer):
    def __init__(self) -> None:
        self.uri = "bolt://localhost:7687"
        self.driver = GraphDatabase.driver(
            self.uri, auth=("neo4j", "holacomoestas"))

    def _create_class(self, tx, name: str) -> None:
        tx.run("CREATE (p:Class {name: $name})", name=name)

    def _create_relation(self, tx, class1: str, class2: str, relation: str) -> None:
        query = f"MATCH(a: Class), (b: Class) WHERE a.name = $class1 AND b.name = $class2 CREATE(a)-[r:{relation}] -> (b)"
        tx.run(query, class1=class1, class2=class2)

    def delete_all(self) -> None:
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")

    def close(self):
        # Cierra la conexión con la base de datos
        self.driver.close()

    @override
    def on_class_found(self, class_name: str) -> None:
        # agregar un nodo
        with self.driver.session() as session:
            session.execute_write(self._create_class, class_name)

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str) -> None:
        # agregar relacion
        with self.driver.session() as session:
            session.execute_write(self._create_relation,
                                  class1, class2, relation)
