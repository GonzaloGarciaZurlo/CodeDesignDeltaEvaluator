from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor
from parser_puml.puml_observer import Observer
from parser_puml import constants

grammar = Grammar(
    r"""
    start               = ( name_space / class_definition / comment / directive / relationship / other)*

    name_space           = ws? "namespace" ws? class_name ws? "{"? ws?

    class_definition    = ws? "class" ws class_name ws? alias? ws? "{"? ws?

    class_name          = ~r'"?[A-Za-z_][A-Za-z0-9_.]*"?'   # Captura nombres con o sin comillas

    alias               = "as" ws class_name               # Alias con la palabra clave 'as'

    # Definición de los tipos de relaciones
    relationship_type   = '--|>' / '<|--' / '..|>' / '<|..' / '-->' / '<--' / '*--' / '--*' / 'o--' / '--o' / '--'
    
    relationship        = class_name ws* relationship_type ws* class_name ws?

    comment             = ~r"/'.*?'/"
    
    directive           = ~r"set\s+\S+\s+\S+" ws?  # Directivas como 'set <clave> <valor>'
    
    other               = ~r".*\n?"  # Captura cualquier otra línea, permitiendo contenido arbitrario
    ws                  = ~r"\s+"                                 # Espacios en blanco
    """
)


class Parsimonius(NodeVisitor):
    def __init__(self, observer: Observer):
        self.namespace = ""
        self.observer = observer

    def parse_uml(self, file: str) -> None:
        with open(file, 'r', encoding='utf-8') as filename:
            content = filename.read()
            tree = grammar.parse(content)
            self.visit(tree)

    def visit_name_space(self, node, visited_children):
        self.namespace = visited_children[3]
        print(f"Namespace found: {self.namespace}")

    def visit_class_definition(self, node, visited_children):
        class_name = visited_children[3]
        if len(visited_children[5]) > 0:
            alias = visited_children[5][0]
            self.observer.on_class_found(alias)
        else:
            self.observer.on_class_found(class_name)

    def visit_class_name(self, node, visited_children):
        return node.text.strip('"')

    def visit_alias(self, node, visited_children):
        return visited_children[2]

    def visit_alias_name(self, node, visited_children):
        return node.text.strip('"')

    def visit_relationship_type(self, node, visited_children):
        return str(node.text)

    def visit_relationship(self, node, visited_children):
        class_a = str(visited_children[0])
        rel_type = str(visited_children[2])
        class_b = str(visited_children[4])

        if self.namespace != "" and self.namespace in class_a:
            class_a = class_a.replace(self.namespace + ".", "")
        if self.namespace != "" and self.namespace in class_b:
            class_b = class_b.replace(self.namespace + ".", "")

        rel_type = constants.convert_relation(rel_type)
        if "2" in rel_type:
            self.observer.on_relation_found(class_b, class_a, rel_type)
        else:
            self.observer.on_relation_found(class_a, class_b, rel_type)

    def generic_visit(self, node, visited_children):
        # Fallback for any other nodes not explicitly visited
        return visited_children or node.text
