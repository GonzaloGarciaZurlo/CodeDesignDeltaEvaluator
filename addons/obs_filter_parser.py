"""
This module contains the Filter class,
this class is an intermediate Observer that filters the information it receives.
"""
from collections import Counter
import re
from overrides import override
from api import CddeAPI
from puml_observer import Observer


class Filter(Observer):
    """
    Observer class that filters the information it receives.
    """

    def __init__(self, observer_to_send: Observer) -> None:
        self.observer_to_send = observer_to_send
        self.classes = []
        self.relationships = []
        self.packages = []

    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened
        """

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed
        """
        self.filter()
        self.send()

    @override
    def on_class_found(self, class_name: str, kind, label: str) -> None:
        """
        Print the class found
        """
        self.classes.append([class_name, kind, label])

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str, label: str) -> None:
        """
        Print the relationship found
        """
        self.relationships.append([class1, class2, relation, label])

    @override
    def on_package_found(self, package_name: str, classes: list,  label: str) -> None:
        """
        Print the package found
        """
        self.packages.append([package_name, classes, label])

    def filter(self) -> None:
        """
        Filter the information received
        """
        self.filter_classes()
        self.filter_relationships()
        self.filter_packages()

    def filter_relationships(self) -> None:
        """
        Filter the relationships
        - If any class perteneces to a namespace or package, the namespace or package is removed from the class name
        - Removing special characters of the class names
        """
        self._delete_ns_or_pkg("relationships")
        self._remove_special_characters("relationships")

    def filter_classes(self) -> None:
        """
        Filter the classes:
        - Removing duplicates
        - If any class perteneces to a namespace or package, the namespace or package is removed from the class name
        - Removing special characters of the class names
        """
        self._delete_ns_or_pkg("classes")
        self._remove_special_characters("classes")
        self._remove_one_duplicate_classname()

    def filter_packages(self) -> None:
        """
        Filter the classes in thepackages
        """
        self._delete_ns_or_pkg("packages")
        self._remove_special_characters("packages")

    def _delete_ns_or_pkg(self, option: str) -> None:
        """
        Delete the namespace or package of the class names
        """
        if option == "classes":
            for i in range(len(self.classes)):
                class_name, kind, label = self.classes[i]
                if '.' in class_name:
                    self.classes[i][0] = class_name.split('.')[-1]
        elif option == "relationships":
            for i in range(len(self.relationships)):
                class1, class2, relation, label = self.relationships[i]
                if '.' in class1:
                    self.relationships[i][0] = class1.split('.')[-1]
                if '.' in class2:
                    self.relationships[i][1] = class2.split('.')[-1]
        elif option == "packages":
            for i in range(len(self.packages)):
                package_name, classes, label = self.packages[i]
                for j in range(len(classes)):
                    if '.' in classes[j]:
                        self.packages[i][1][j] = classes[j].split('.')[-1]

    def _remove_special_characters(self, option: str) -> None:
        """
        Remove special characters from the class name
        """
        if option == "classes":
            for i in range(len(self.classes)):
                re.sub(r'[^A-Za-z0-9\s]', '', self.classes[i][0])
        elif option == "relationships":
            for i in range(len(self.relationships)):
                re.sub(r'[^A-Za-z0-9\s]', '', self.relationships[i][0])
                re.sub(r'[^A-Za-z0-9\s]', '', self.relationships[i][1])
        elif option == "packages":
            for i in range(len(self.packages)):
                for j in range(len(self.packages[i][1])):
                    re.sub(r'[^A-Za-z0-9\s]', '', self.packages[i][1][j])

    def _remove_one_duplicate_classname(self) -> None:
        """
        Remove one duplicate class name
        """
        class_names = [class_name for class_name, kind, label in self.classes]
        count = Counter(class_names)
        for class_name, kind, label in self.classes:
            if count[class_name] > 1:
                count[class_name] -= 1
                self.classes.remove([class_name, kind, label])

    def send(self) -> None:
        """
        Send the filtered information to the next observer
        """
        self._send_classes()
        self._send_relationships()
        self._send_packages()

    def _send_classes(self) -> None:
        """
        Send the filtered classes to the next observer
        """
        for classes in self.classes:
            class_name, kind, label = classes
            self.observer_to_send.on_class_found(class_name, kind, label)

    def _send_relationships(self) -> None:
        """
        Send the filtered relationships to the next observer
        """
        for relationship in self.relationships:
            class1, class2, relation, label = relationship
            self.observer_to_send.on_relation_found(
                class1, class2, relation, label)

    def _send_packages(self) -> None:
        """
        Send the filtered packages to the next observer
        """
        for package in self.packages:
            package_name, classes, label = package
            self.observer_to_send.on_package_found(
                package_name, classes, label)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('filter', Filter)
