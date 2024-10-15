"""
module parser with regex implementation
"""
import re
# from overrides import override
from parser_puml.puml_parser import PumlParser
from parser_puml.constants import CLASS_PATTERN, RELATION_PATTERN, convert_relation


class Regex(PumlParser):
    """
    Class that implements parser with regex to parse the plantuml file
    """

    # @override
    def parse_uml(self, file: str) -> None:
        with open(file, 'r', encoding='utf-8') as filename:
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

            else:  # Caso sin alias
                class_name = match.group(3)
                self.observer.on_class_found(class_name)

    def _parse_relation(self, line: str) -> None:
        # Identificar relaciones entre clases con diferentes tipos de conectores
        match = re.search(RELATION_PATTERN, line)

        if match:
            class_a, relation, class_b = match.groups()
            # Cambiar simbolo a nombre
            relation = convert_relation(relation)
            # Guardar la relación
            if "2" in relation:  # Invertir la relación
                self.observer.on_relation_found(class_b, class_a, relation)
            else:
                self.observer.on_relation_found(class_a, class_b, relation)
