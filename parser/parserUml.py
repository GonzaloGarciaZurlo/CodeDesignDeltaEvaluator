import re
import networkx as nx
import pyreverse_util

class PlantUMLParser:
    def __init__(self, filename):
        self.filename = filename
        self.classes = set()  
        self.relations = []   
        self.graph = nx.DiGraph()  

    def parse(self):
        with open(self.filename, 'r') as file:
            for line in file:
                line = line.strip()
                self._parse_class(line)    # Buscar declaraciones de clases
                self._parse_relation(line) # Buscar relaciones entre clases
        
        self._create_graph()

    def _parse_class(self, line):
        # Identificar declaraciones de clases con o sin alias
        class_pattern = r'class\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|class\s+([\w.]+)'
        match = re.search(class_pattern, line)
        if match:
            if match.group(2):  # Caso con alias
                alias_name = match.group(2)
                self.classes.add(alias_name)
            else:  # Caso sin alias
                class_name = match.group(3)
                self.classes.add(class_name)

    def _parse_relation(self, line):
        # Identificar relaciones entre clases con diferentes tipos de conectores
        relation_pattern = r'(\w+[\w.]+)\s*([-\*<>|]+)\s*(\w+[\w.]+)'
        match = re.search(relation_pattern, line)

        if match:
            class_a, relation, class_b = match.groups()
            if relation == '--|>':  # Herencia
                relation = 'inheritance'
            elif relation == '..|>': # Implementación
                relation = 'implementation'
            elif relation == '-->':  # Dependencia
                relation = 'dependency'
            elif relation == '*--':  # Composición
                relation = 'composition'
            elif relation == 'o--':  # Agregación
                relation = 'aggregation'
            elif relation == '--':  # Asociación
                relation = 'association'
            self.relations.append((class_a, relation, class_b))  # Guardar la relación 

    def _create_graph(self):
        # Añadir las clases como nodos en el grafo
        self.graph.add_nodes_from(self.classes)
        
        # Añadir las relaciones como bordes entre nodos (clases)
        for class_a, relation, class_b in self.relations:
            self.graph.add_edge(class_a, class_b, relation=relation)

    def get_graph(self):
        return self.graph

plantUML = pyreverse_util.generate_plantuml_python('../Samples/SOLID+LoD/I/ISP_P.py')

parser = PlantUMLParser(plantUML)  # Archivo .plantuml
parser.parse()

graph = parser.get_graph()

print("Clases:", list(parser.classes))
print("Relaciones:", parser.relations)

pyreverse_util.delete_plantuml(plantUML)