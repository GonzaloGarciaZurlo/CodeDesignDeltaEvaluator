"""
Module parser with parsimonius implementation
"""
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node
from CodeDesignDeltaEvaluator.factories.puml_observer import Observer
from CodeDesignDeltaEvaluator.factories.puml_parser import PumlParser
from CodeDesignDeltaEvaluator.addons import constants
from CddeAPI import CddeAPI

grammar = Grammar(
    r"""
    start               = ( name_space / class_definition / comment / directive / relationship / other)*

    name_space           = ws? "namespace" ws? class_name ws? "{"? ws?

    class_definition    = ws? "class" ws class_name ws? alias? ws? "{"? ws?

    class_name          = ~r'"?[A-Za-z_][A-Za-z0-9_.]*"?'  

    alias               = "as" ws class_name               

    relationship_type   = '--|>' / '<|--' / '..|>' / '<|..' / '-->' / '<--' / '*--' / '--*' / 'o--' / '--o' / '--'
    
    relationship        = class_name ws* relationship_type ws* class_name ws?

    comment             = ~r"/'.*?'/"
    
    directive           = ~r"set\s+\S+\s+\S+" ws?  
    
    other               = ~r".*\n?"  
    ws                  = ~r"\s+"                                 
    """
)


class Parsimonius(NodeVisitor):
    """
    Class that implements parser with parsimonius to parse the plantuml file
    """

    def __init__(self, observer: Observer):
        self.namespace = ""
        self.observer = observer

    def parse_uml(self, file: str) -> None:
        """ 
        Parse the plantuml file
        """
        with open(file, 'r', encoding='utf-8') as filename:
            content = filename.read()
            tree = grammar.parse(content)
            self.visit(tree)

    def visit_name_space(self, node: Node, visited_children: list) -> None:
        """
        Set namespace name
        """
        self.namespace = visited_children[3]

    def visit_class_definition(self, node: Node, visited_children: list) -> None:
        """
        Identify class declarations with or without aliases
        """
        class_name = visited_children[3]
        if len(visited_children[5]) > 0:
            alias = visited_children[5][0]
            self.observer.on_class_found(alias)
        else:
            self.observer.on_class_found(class_name)

    def visit_class_name(self, node: Node, visited_children: list) -> str:
        """
        Extract class name without quotes
        """
        return node.text.strip('"')

    def visit_alias(self, node: Node, visited_children: list) -> str:
        """
        Extract alias name
        """
        return visited_children[2]

    def visit_alias_name(self, node: Node, visited_children: list) -> str:
        """
        Extract alias name without quotes
        """
        return node.text.strip('"')

    def visit_relationship_type(self, node: Node, visited_children: list) -> str:
        """
        Extract relationship type
        """
        return str(node.text)

    def visit_relationship(self, node: Node, visited_children: list) -> None:
        """
        Identify relationships between classes with different types of connectors
        """
        class_a = str(visited_children[0])
        rel_type = str(visited_children[2])
        class_b = str(visited_children[4])

        # Remove namespace from class names
        class_a = self._delete_namespace(class_a)
        class_b = self._delete_namespace(class_b)

        # Convert relationship type to standard names
        rel_type = constants.convert_relation(rel_type)
        if "2" in rel_type:
            self.observer.on_relation_found(class_b, class_a, rel_type)
        else:
            self.observer.on_relation_found(class_a, class_b, rel_type)

    def generic_visit(self, node: Node, visited_children: list) -> str:
        """
        Fallback for any other nodes not explicitly visited
        """
        return visited_children or node.text

    def _delete_namespace(self, class_name: str) -> str:
        """
        Remove namespace from class names
        """
        if self.namespace != "" and self.namespace in class_name:
            class_name = class_name.replace(self.namespace + ".", "")
            class_name = class_name.replace('"', "")
        return class_name


def init_module(api: CddeAPI) -> None:
    api.register_puml_parser('parsimonious', Parsimonius())
