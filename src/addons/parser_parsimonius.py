"""
Module parser with parsimonius implementation.
In this module we define the parser with parsimonius to parse the plantuml file.
Contains the grammar and the class that implements the parser.
"""
from typing import Any  # type: ignore[import-untyped]  # pylint: disable=import-error
# type: ignore[import-untyped]   # pylint: disable=import-error
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node
from src.cdde.addons_api import CddeAPI
from src.cdde.puml_observer import Observer, MethodKind
from src.cdde.constants import convert_relation, convert_class_kind, Direction, convert_visibility


class Parsimonius(NodeVisitor):
    """
    Class that implements parser with parsimonius to parse the plantuml file.
    """

    def __init__(self, observer: Observer, file_grammar: str) -> None:
        self.observer = observer
        self.file_grammar = file_grammar
        self.grammar = self._init_grammar()

    def _init_grammar(self) -> Grammar:
        """
        Initialize the grammar.
        """
        with open(self.file_grammar, 'r', encoding='utf-8') as grammar_file:
            grammar_text = grammar_file.read()
        return Grammar(grammar_text)

    def parse_uml(self, file: str) -> None:
        """ 
        Main method to parse the plantuml file.
        """
        with open(file, 'r', encoding='utf-8') as filename:
            self.observer.open_observer()
            content = filename.read()
            tree = self.grammar.parse(content)
            self.visit(tree)
            self.observer.close_observer()

    def visit_package(self, _node: Node, visited_children: list) -> None:
        """
        Extract package name.
        """
        package_name = visited_children[3]
        classes = []
        for declaration in visited_children[7]:
            classes.append(declaration)
        self.observer.on_package_found(package_name, classes)

    def visit_namespace(self, _node: Node, visited_children: list) -> None:
        """
        Extract namespace name.
        """
        namespace_name = visited_children[3]
        classes = []
        for declaration in visited_children[7]:
            classes.append(declaration)
        self.observer.on_package_found(namespace_name, classes)

    def visit_class_definition(self, _node: Node, visited_children: list) -> str:
        """
        Identify class declarations with or without aliases,
        after that, notify the observer about the class found.
        """
        class_type = visited_children[1][0]
        class_type = convert_class_kind(class_type)

        class_name = visited_children[3]
        if len(visited_children[5]) > 0:
            class_name = visited_children[5][0]  # alias
            self.observer.on_class_found(class_name, class_type)
        else:
            self.observer.on_class_found(class_name, class_type)

        # Send methods to observer
        for method in visited_children[11]:
            if method != "":
                kind = method[0]
                method_name = method[1:]
                self.observer.on_method_found(
                    class_name, method_name, convert_visibility(kind))

        return class_name

    def visit_name(self, node: Node, _visited_children: list) -> str:
        """
        Extract class name without quotes.
        """
        return node.text.strip('"')

    def visit_class_name(self, node: Node, _visited_children: list) -> str:
        """
        Extract class name without quotes and spaces.
        """
        node.text.strip('"')
        return node.text.strip(' ')

    def visit_alias(self, _node: Node, visited_children: list) -> str:
        """
        Extract alias name.
        """
        return visited_children[2]

    def visit_relationship_type(self, node: Node, _visited_children: list) -> str:
        """
        Extract relationship type.
        """
        return str(node.text)

    def visit_relationship(self, _node: Node, visited_children: list) -> None:
        """
        Identify relationships between classes with different types of connectors.
        After that, notify the observer about the relationship found.
        """
        class_a = str(visited_children[0])
        rel_type = str(visited_children[2])
        class_b = str(visited_children[4])

        # Convert relationship type to standard names
        rel_type, reverse = convert_relation(rel_type)
        if reverse == Direction.BACKWARD:
            self.observer.on_relation_found(
                class_b, class_a, rel_type)
        else:
            self.observer.on_relation_found(
                class_a, class_b, rel_type)

    def visit_body(self, _node: Node, visited_children: list) -> str:
        """
        Extract method name.
        """
        return str(visited_children[0])

    def visit_method(self, _node: Node, visited_children: list) -> str:
        """
        return method name, without arguments and return type.
        """
        return str(visited_children[0]) + str(visited_children[2])

    def visit_visibility(self, node: Node, _visited_children: list) -> MethodKind:
        """
        Convert visibility symbols to names.
        """
        return node.text.strip()

    def visit_attribute(self, _node: Node, visited_children: list) -> str:
        """
        Ignore attributes.
        """
        return ""

    def visit_comment(self, _node: Node, _visited_children: list) -> str:
        """
        Ignore comments.
        """
        return ""

    def generic_visit(self, node: Node, visited_children: list) -> list[Any] | Any:
        """
        Fallback for any other nodes not explicitly visited.
        """
        return visited_children or node.text


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_parser('parsimonious', Parsimonius)
