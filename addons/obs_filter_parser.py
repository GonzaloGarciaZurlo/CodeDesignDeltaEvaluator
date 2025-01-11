"""
This module contains the Filter class,
this class is an intermediate Observer that filters the information it receives.
"""
import re
from typing import Final
from overrides import override
from api import CddeAPI
from puml_observer import Observer


class Filter(Observer):
    """
    Observer class that filters the information it receives.
    Contains the methods to filter the classes, relationships and packages.
    Coordinates the creation of its subclasses
    and calls their corresponding methods to filter what is necessary
    """

    def __init__(self, observer_to_send: Observer,
                 classes=None, relationships=None, packages=None) -> None:
        self.observer_to_send: Final = observer_to_send
        self.classes: list = classes if classes is not None else []
        self.relationships: list = relationships if relationships is not None else []
        self.packages: list = packages if packages is not None else []

    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened
        This method creates the childs filters
        """

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed
        """
        class_filter = ClassFilter(
            self.classes, self.observer_to_send)
        relationship_filter = RelationshipFilter(
            self.relationships, self.observer_to_send)
        package_filter = PackageFilter(
            self.packages, self.observer_to_send)

        # Filter the information
        class_filter.filter()
        relationship_filter.filter()
        package_filter.filter()
        # Send the filtered information
        class_filter.send()
        relationship_filter.send()
        package_filter.send()

    @override
    def on_class_found(self, class_name: str, kind, label: str) -> None:
        """
        Create a list with the class found
        """
        self.classes.append([class_name, kind, label])

    @override
    def on_relation_found(self, class1: str, class2: str, relation: str, label: str) -> None:
        """
        Create a list with the relationship found
        """
        self.relationships.append([class1, class2, relation, label])

    @override
    def on_package_found(self, package_name: str, classes: list,  label: str) -> None:
        """
        Create a list with the package found
        """
        self.packages.append([package_name, classes, label])


class ClassFilter(Filter):
    """
    Filter the classes 
    """

    def __init__(self, classes: list, observer_to_send: Observer) -> None:
        super().__init__(observer_to_send, classes=classes)

    def filter(self) -> None:
        """
        Filter the classes:
        - Removing duplicates
        - If any class perteneces to a namespace or package, 
        the namespace or package is removed from the class name
        - Removing special characters of the class names
        """
        self._delete_ns_or_pkg()
        self._remove_special_characters()
        self._remove_duplicates()

    def _delete_ns_or_pkg(self) -> None:
        """
        Delete the namespace or package of the class names
        """
        for i, c in enumerate(self.classes):
            class_name, _, _ = c
            if '.' in class_name:
                self.classes[i][0] = class_name.split('.')[-1]

    def _remove_special_characters(self) -> None:
        """
        Remove special characters from the class name
        """
        for i, c in enumerate(self.classes):
            self.classes[i][0] = re.sub(r'[^A-Za-z0-9\s]', '', c[0])

    def _remove_duplicates(self) -> None:
        """
        Remove duplicate class names, keeping only the first occurrence.
        """
        seen = set()
        filtered_classes = []

        for class_name, kind, label in self.classes:
            if class_name not in seen:
                seen.add(class_name)
                filtered_classes.append([class_name, kind, label])

        self.classes = filtered_classes

    def send(self) -> None:
        """
        Send the filtered classes to the next observer
        """
        for classes in self.classes:
            class_name, kind, label = classes
            self.observer_to_send.on_class_found(class_name, kind, label)


class RelationshipFilter(Filter):
    """
    Class that filters the relationships
    """

    def __init__(self, relationships: list, observer_to_send: Observer) -> None:
        super().__init__(observer_to_send, relationships=relationships)

    def filter(self) -> None:
        """
        Filter the relationships
        - If any class perteneces to a namespace or package, 
        the namespace or package is removed from the class name
        - Removing special characters of the class names
        """
        self._delete_ns_or_pkg()
        self._remove_special_characters()

    def _delete_ns_or_pkg(self) -> None:
        """
        Delete the namespace or package of the class names
        """
        for i, relation in enumerate(self.relationships):
            class1, class2, _, _ = relation
            if '.' in class1:
                self.relationships[i][0] = class1.split('.')[-1]
            if '.' in class2:
                self.relationships[i][1] = class2.split('.')[-1]

    def _remove_special_characters(self) -> None:
        """
        Remove special characters from the class name
        """
        for i, relation in enumerate(self.relationships):
            self.relationships[i][0] = re.sub(
                r'[^A-Za-z0-9\s]', '', relation[0])
            self.relationships[i][1] = re.sub(
                r'[^A-Za-z0-9\s]', '', relation[1])

    def send(self) -> None:
        """
        Send the filtered relationships to the next observer
        """
        for relationship in self.relationships:
            class1, class2, relation, label = relationship
            self.observer_to_send.on_relation_found(
                class1, class2, relation, label)


class PackageFilter(Filter):
    """
    Class that filters the packages
    """

    def __init__(self, packages: list, observer_to_send: Observer) -> None:
        super().__init__(observer_to_send, packages=packages)

    def filter(self) -> None:
        """
        Filter the classes in the packages
        """
        self._delete_ns_or_pkg()
        self._remove_special_characters()
        self._remove_duplicates()

    def _delete_ns_or_pkg(self) -> None:
        """
        Delete the namespace or package of the class names
        """
        for i, package in enumerate(self.packages):
            _, classes, _ = package
            for j, c in enumerate(classes):
                if '.' in c:
                    self.packages[i][1][j] = c.split('.')[-1]

    def _remove_special_characters(self) -> None:
        """
        Remove special characters from the class name
        """
        for i, package in enumerate(self.packages):
            for j, c in enumerate(package[1]):
                self.packages[i][1][j] = re.sub(r'[^A-Za-z0-9\s]', '', c)

    def _remove_duplicates(self) -> None:
        """
        Remove duplicate class names, keeping only the first occurrence.
        """
        for i, package in enumerate(self.packages):
            _, classes, _ = package
            seen = set()
            filtered_classes = []

            for class_name in classes:
                if class_name not in seen:
                    seen.add(class_name)
                    filtered_classes.append(class_name)

            self.packages[i][1] = filtered_classes

    def send(self) -> None:
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
