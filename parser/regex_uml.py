import re
import time
from parser.puml_observer import Observer
from parser.puml_parser import PUML_Parser
from overrides import override
from parser.constants import CLASS_PATTERN, RELATION_PATTERN, ABS_CLASS_PATTERN, ABS_PATTERN

class Regex(PUML_Parser):
    def __init__(self, observer: Observer) -> None:
        super().__init__(observer)

#   @override
    def parse(self, filename: str) -> None:
        with open(filename, 'r') as filename:
            for line in filename:
                line = line.strip()
                self._parse_class(line)    # Buscar declaraciones de clases
                self._parse_relation(line)  # Buscar relaciones entre clases

    def _parse_class(self, line: str) -> None:
        # Identificar declaraciones de clases con o sin alias
        match = re.search(CLASS_PATTERN, line)
        if match:
            if match.group(2):  # Caso con alias
                alias_name = match.group(2)
                self.observer.on_class_found(alias_name)
                # time.sleep(1)
            else:  # Caso sin alias
                class_name = match.group(3)
                self.observer.on_class_found(class_name)
                # time.sleep(1)

    def _parse_relation(self, line: str) -> None:
        # Identificar relaciones entre clases con diferentes tipos de conectores
        match = re.search(RELATION_PATTERN, line)

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
            # time.sleep(1)
