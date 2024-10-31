"""
module parser with regex implementation
"""
import re
# from overrides import override
from api import CddeAPI
from puml_observer import Observer
from puml_parser import PumlParser
from constants import CLASS_PATTERN, RELATION_PATTERN, NAME_SPACE_PATTERN, ABS_CLASS_PATTERN
from constants import convert_relation


class Regex(PumlParser):
    """
    Class that implements parser with regex to parse the plantuml file
    """

    def __init__(self, observer: Observer) -> None:
        super().__init__(observer)
        self.namespace = ""

    # @override
    def parse_uml(self, file: str) -> None:
        """
        Parse the plantuml file
        """
        with open(file, 'r', encoding='utf-8') as filename:
            self.observer.open_observer()
            for line in filename:
                line = line.strip()
                # Search for namespace declarations
                self._set_namespace(line)
                # Search for abstract class declarations
                self._parse_abstract_class(line)
                # Search for class declarations
                self._parse_class(line)
                # Finding relationships between classes
                self._parse_relation(line)
            self.observer.close_observer()

    def _parse_class(self, line: str) -> None:
        """
        Identify class declarations with or without aliases
        """
        match = re.search(CLASS_PATTERN, line)
        if match:
            if match.group(2):  # Case with alias
                alias_name = match.group(2)
                self.observer.on_class_found(alias_name, "class")

            else:  # Case without alias
                class_name = match.group(3)
                self.observer.on_class_found(class_name, "class")

    def _parse_abstract_class(self, line: str) -> None:
        """
        Identify abstract class declarations with or without aliases
        """
        match = re.search(ABS_CLASS_PATTERN, line)
        if match:
            if match.group(3):
                alias_name = match.group(3)
                self.observer.on_class_found(alias_name, "abstract")
            else:
                class_name = match.group(4)
                self.observer.on_class_found(class_name, "abstract")

    def _parse_relation(self, line: str) -> None:
        """
        Identify relationships between classes with different types of connectors
        """
        match = re.search(RELATION_PATTERN, line)
        if match:
            class_a, relation, class_b = match.groups()
            class_a = self._delete_namespace(class_a)
            class_b = self._delete_namespace(class_b)
            relation = convert_relation(relation)

            if "2" in relation:  # Reverse the relationship
                self.observer.on_relation_found(class_b, class_a, relation)
            else:
                self.observer.on_relation_found(class_a, class_b, relation)

    def _set_namespace(self, line: str) -> None:
        """
        Set namespace name
        """
        match = re.search(NAME_SPACE_PATTERN, line)
        if match:
            namespace = match.group(1)
            self.namespace = namespace

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
    Initialize the module on the API.
    """
    api.register_puml_parser('regex', Regex)
