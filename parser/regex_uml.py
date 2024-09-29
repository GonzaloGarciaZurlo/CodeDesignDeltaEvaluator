import puml_parser
import puml_observer
import re
import time


class Regex(puml_parser.PUML_Parser):
    def __init__(self, observer: puml_observer.Observer) -> None:
        super().__init__(observer)

    def parse(self, filename: str) -> None:
        with open(filename, 'r') as filename:
            for line in filename:
                line = line.strip()
                self._parse_class(line)    # Buscar declaraciones de clases
                self._parse_relation(line)  # Buscar relaciones entre clases

    def _parse_class(self, line: str) -> None:
        # Identificar declaraciones de clases con o sin alias
        class_pattern = r'class\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|class\s+([\w.]+)'
        match = re.search(class_pattern, line)
        if match:
            if match.group(2):  # Caso con alias
                alias_name = match.group(2)
                self.observer.on_class_found(alias_name)
                time.sleep(1)
            else:  # Caso sin alias
                class_name = match.group(3)
                self.observer.on_class_found(class_name)
                time.sleep(1)

    def _parse_relation(self, line: str) -> None:
        # Identificar relaciones entre clases con diferentes tipos de conectores
        relation_pattern = r'(\w+[\w.]+)\s*([-\*<>|]+)\s*(\w+[\w.]+)'
        match = re.search(relation_pattern, line)

        if match:
            class_a, relation, class_b = match.groups()
            if relation == '--|>':  # Herencia
                relation = 'inheritance'
            elif relation == '..|>':  # Implementación
                relation = 'implementation'
            elif relation == '-->':  # Dependencia
                relation = 'dependency'
            elif relation == '*--':  # Composición
                relation = 'composition'
            elif relation == 'o--':  # Agregación
                relation = 'aggregation'
            elif relation == '--':  # Asociación
                relation = 'association'
            # Guardar la relación
            self.observer.on_relation_found(class_a, class_b, relation)
            time.sleep(1)
