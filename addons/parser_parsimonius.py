"""
Module parser with parsimonius implementation
"""
from typing import Any
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node
from api import CddeAPI
from puml_observer import Observer
import constants


grammar = Grammar(
    r"""
    start               = ( package_namespace / class_definition / relationship / other)*

    package_namespace   = package / namespace

    package             = ws? "package" ws? name ws? "{" ws? class_definition+ ws? "}"

    namespace           = ws? "namespace" ws? name ws? "{" ws? class_definition+ ws? "}"

    class_type          = "class" / "interface" / "struct" / "abstract class" / "abstract" 

    class_name          = ~r'"[^"]*"|\'[^\']*\'|[^\s]+'

    class_definition    = ws? class_type ws class_name ws? alias? ws? stereotype? ws? "{" ws? body* ws? "}"

    name                = ~r'"?[A-Za-z_#[][A-Za-z0-9_.#\[\]]*"?'

    method_name         = ws? ~r'"?[A-Za-z_#[(][A-Za-z0-9_.#\[\]()]*"?' ws?

    alias               = "as" ws name       

    body                =  method / comment / method_name 

    method              = visibility ws? ~"[^\n]+" ws?

    visibility          = ("+" / "-" / "#")        

    stereotype          = "<<" ws? "(" ws? name ws? "," ws? name ws? ")" ws? ">>"

    relationship_type   = '--|>' / '<|--' / '..|>' / '<|..' / '-->' / '<--' / '*--' / '--*' / 'o--' / '--o' / '--'
    
    relationship        = name ws* relationship_type ws* name ws?

    comment             = ws? "'" ~"[^\n]*"
    
    other               = ~r".*\n?"  

    ws                  = ~r"\s+"                                 
    """
)


class Parsimonius(NodeVisitor):
    """
    Class that implements parser with parsimonius to parse the plantuml file
    """

    def __init__(self, observer: Observer, label: str) -> None:
        self.observer = observer
        self.label = label

    def parse_uml(self, file: str) -> None:
        """ 
        Parse the plantuml file
        """
        with open(file, 'r', encoding='utf-8') as filename:
            self.observer.open_observer()
            content = filename.read()
            tree = grammar.parse(content)
            self.visit(tree)
            self.observer.close_observer()

    def visit_package(self, node: Node, visited_children: list) -> None:
        """
        Extract package name
        """
        package_name = visited_children[3]
        classes = []
        for declaration in visited_children[7]:
            classes.append(declaration)
        self.observer.on_package_found(package_name, classes, self.label)

    def visit_namespace(self, node: Node, visited_children: list) -> None:
        """
        Extract namespace name
        """
        namespace_name = visited_children[3]
        classes = []
        for declaration in visited_children[7]:
            classes.append(declaration)
        self.observer.on_package_found(namespace_name, classes, self.label)

    def visit_class_definition(self, node: Node, visited_children: list) -> str:
        """
        Identify class declarations with or without aliases
        """
        class_type = visited_children[1][0]
        if class_type == "abstract class":
            class_type = "abstract"
        class_name = visited_children[3]
        if len(visited_children[5]) > 0:
            alias = visited_children[5][0]
            self.observer.on_class_found(alias, class_type, self.label)
            return alias
        self.observer.on_class_found(class_name, class_type, self.label)
        return class_name

    def visit_name(self, node: Node, visited_children: list) -> str:
        """
        Extract class name without quotes
        """
        return node.text.strip('"')

    def visit_class_name(self, node: Node, visited_children: list) -> str:
        """
        Extract class name without quotes and spaces
        """
        node.text.strip('"')
        return node.text.strip(' ')

    def visit_alias(self, node: Node, visited_children: list) -> str:
        """
        Extract alias name
        """
        return visited_children[2]

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

        # Convert relationship type to standard names
        rel_type = constants.convert_relation(rel_type)
        if "2" in rel_type:
            rel_type = rel_type.replace("2", "")
            self.observer.on_relation_found(
                class_b, class_a, rel_type, self.label)
        else:
            self.observer.on_relation_found(
                class_a, class_b, rel_type, self.label)

    def generic_visit(self, node: Node, visited_children: list) -> list[Any] | Any:
        """
        Fallback for any other nodes not explicitly visited
        """
        return visited_children or node.text


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API
    """
    api.register_puml_parser('parsimonius', Parsimonius)
