"""
Module parser with parsimonius implementation
"""
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor, Node
from api import CddeAPI
from puml_observer import Observer
import constants

grammar = Grammar(
    r"""
    start               = ( class_definition / abstract_definition / interface_definition / struct_definition / comment / directive / relationship / other)*


    class_definition    = ws? "class" ws class_name ws? alias? ws? "{"? ws?

    abstract_definition = ws? abstract_class ws class_name ws? alias? ws? "{"? ws?

    interface_definition = ws? "interface" ws class_name ws? alias? ws? "{"? ws?

    struct_definition   = ws? "struct" ws class_name ws? alias? ws? "{"? ws?

    abstract_class      = "abstract class"/ "abstract" 

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

    def __init__(self, observer: Observer, label: str) -> None:
        self.namespace = ""
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

    def visit_class_definition(self, node: Node, visited_children: list) -> None:
        """
        Identify class declarations with or without aliases
        """
        class_name = visited_children[3]
        if len(visited_children[5]) > 0:
            alias = visited_children[5][0]
            self.observer.on_class_found(alias, "Class", self.label)
        else:
            self.observer.on_class_found(class_name, "Class", self.label)

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
        return visited_children[2].strip('"')

    def visit_abstract_definition(self, node: Node, visited_children: list) -> None:
        """
        Identify abstract class declarations with or without aliases
        """
        class_name = visited_children[3]
        if len(visited_children[5]) > 0:
            alias = visited_children[5][0]
            self.observer.on_class_found(alias, "Abstract", self.label)
        else:
            self.observer.on_class_found(class_name, "Abstract", self.label)

    def visit_interface_definition(self, node: Node, visited_children: list) -> None:
        """
        Identify interface declarations with or without aliases
        """
        class_name = visited_children[3]
        if len(visited_children[5]) > 0:
            alias = visited_children[5][0]
            self.observer.on_class_found(alias, "Interface", self.label)
        else:
            self.observer.on_class_found(class_name, "Interface", self.label)

    def visit_relationship_type(self, node: Node, visited_children: list) -> str:
        """
        Extract relationship type
        """
        return str(node.text)

    def visit_class_name_without_dot(self, node: Node, visited_children: list) -> str:
        """
        Extract class name in "someting.Class" format
        """
        return visited_children[1]

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
            rel_type = rel_type.replace("2", "")
            self.observer.on_relation_found(
                class_b, class_a, rel_type, self.label)
        else:
            self.observer.on_relation_found(
                class_a, class_b, rel_type, self.label)

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
    """
    Initialize the module on the API
    """
    api.register_puml_parser('parsimonius', Parsimonius)
