"""
This module contains the Filter class,
this class is an intermediate Observer that filters the information it receives.
"""
import re
from typing import Final
from overrides import override
from src.cdde.addons_api import CddeAPI
from src.cdde.puml_observer import Observer, Modes, ClassKind, Relationship


class Filter(Observer):
    """
    Observer class that filters the information it receives.
    Contains the methods to filter the classes, relationships and packages.
    Coordinates the creation of its subclasses
    and calls their corresponding methods to filter what is necessary.
    """

    def __init__(self, observer_to_send: Observer,
                 classes=None, relationships=None, packages=None, methods=None) -> None:
        self.observer_to_send: Final = observer_to_send
        self.classes: list = self._default_list(classes)
        self.relationships: list = self._default_list(relationships)
        self.packages: list = self._default_list(packages)
        self.methods: list = self._default_list(methods)

    @staticmethod
    def _default_list(value):
        return value if value is not None else []

    @override
    def set_mode(self, mode: Modes) -> None:
        """
        Set the mode of the observer.
        """
        self.observer_to_send.set_mode(mode)

    @override
    def open_observer(self) -> None:
        """
        Event triggered when the observer is opened
        This method creates the childs filters.
        """
        self.observer_to_send.open_observer()

    @override
    def close_observer(self) -> None:
        """
        Event triggered when the observer is closed.
        """
        class_filter = ClassFilter(
            self.classes, self.observer_to_send)
        relationship_filter = RelationshipFilter(
            self.relationships, self.observer_to_send)
        package_filter = PackageFilter(
            self.packages, self.observer_to_send)
        method_filter = MethodsFilter(self.methods, self.observer_to_send)

        # Filter the information
        class_filter.filter()
        relationship_filter.filter()
        package_filter.filter()
        method_filter.filter()

        # Send the filtered information
        class_filter.send()
        relationship_filter.send()
        package_filter.send()
        method_filter.send()

        # Close the observer
        self.observer_to_send.close_observer()

    @override
    def on_class_found(self, class_name: str, kind: ClassKind) -> None:
        """
        Create a list with the class found.
        """
        self.classes.append([class_name, kind])

    @override
    def on_relation_found(self, class1: str, class2: str, relation: Relationship) -> None:
        """
        Create a list with the relationship found.
        """
        self.relationships.append([class1, class2, relation])

    @override
    def on_package_found(self, package_name: str, classes: list) -> None:
        """
        Create a list with the package found.
        """
        self.packages.append([package_name, classes])

    @override
    def on_method_found(self, class_name: str, method_name: str) -> None:
        """
        Create a list with the method found.
        """
        self.methods.append([class_name, method_name])


class ClassFilter(Filter):
    """
    Filter the classes.
    """

    def __init__(self, classes: list, observer_to_send: Observer) -> None:
        super().__init__(observer_to_send, classes=classes)

    def filter(self) -> None:
        """
        Filter the classes:
        - Removing duplicates.
        - If any class perteneces to a namespace or package, 
        the namespace or package is removed from the class name.
        - Removing special characters of the class names.
        """
        self._delete_ns_or_pkg()
        self._remove_special_characters()
        self._remove_duplicates()

    def _delete_ns_or_pkg(self) -> None:
        """
        Delete the namespace or package of the class names.
        """
        for i, c in enumerate(self.classes):
            class_name, _ = c
            self.classes[i][0] = self.__delete_before_last_dot(class_name)

    def __delete_before_last_dot(self, class_name: str) -> str:
        """
        Delete the string before the last dot.
        """
        return class_name.split('.')[-1] if '.' in class_name else class_name

    def _remove_special_characters(self) -> None:
        """
        Remove special characters from the class name.
        """
        for i, c in enumerate(self.classes):
            self.classes[i][0] = re.sub(r'[^A-Za-z0-9\s]', '', c[0])

    def _remove_duplicates(self) -> None:
        """
        Remove duplicate class names, keeping only the first occurrence.
        """
        seen = set()
        filtered_classes = []

        for class_name, kind in self.classes:
            if class_name not in seen:
                seen.add(class_name)
                filtered_classes.append([class_name, kind])

        self.classes = filtered_classes

    def send(self) -> None:
        """
        Send the filtered classes to the next observer.
        """
        for classes in self.classes:
            class_name, kind = classes
            self.observer_to_send.on_class_found(class_name, kind)


class RelationshipFilter(Filter):
    """
    Class that filters the relationships.
    """

    def __init__(self, relationships: list, observer_to_send: Observer) -> None:
        super().__init__(observer_to_send, relationships=relationships)

    def filter(self) -> None:
        """
        Filter the relationships
        - If any class perteneces to a namespace or package, 
        the namespace or package is removed from the class name.
        - Removing special characters of the class names.
        """
        self._delete_ns_or_pkg()
        self._remove_special_characters()

    def _delete_ns_or_pkg(self) -> None:
        """
        Delete the namespace or package of the class names.
        """
        for i, relation in enumerate(self.relationships):
            class1, class2, _ = relation
            self.relationships[i][0] = self.__delete_before_last_dot(class1)
            self.relationships[i][1] = self.__delete_before_last_dot(class2)

    def __delete_before_last_dot(self, class_name: str) -> str:
        """
        Delete the string before the last dot.
        """
        return class_name.split('.')[-1] if '.' in class_name else class_name

    def _remove_special_characters(self) -> None:
        """
        Remove special characters from the class name.
        """
        for i, relation in enumerate(self.relationships):
            self.relationships[i][0] = re.sub(
                r'[^A-Za-z0-9\s]', '', relation[0])
            self.relationships[i][1] = re.sub(
                r'[^A-Za-z0-9\s]', '', relation[1])

    def send(self) -> None:
        """
        Send the filtered relationships to the next observer.
        """
        for relationship in self.relationships:
            class1, class2, relation = relationship
            self.observer_to_send.on_relation_found(
                class1, class2, relation)


class PackageFilter(Filter):
    """
    Class that filters the packages.
    """

    def __init__(self, packages: list, observer_to_send: Observer) -> None:
        super().__init__(observer_to_send, packages=packages)

    def filter(self) -> None:
        """
        Filter the classes in the packages.
        """
        self._delete_ns_or_pkg()
        self._remove_special_characters()
        self._remove_duplicates()

    def _delete_ns_or_pkg(self) -> None:
        """
        Delete the namespace or package of the class names.
        """
        for i, package in enumerate(self.packages):
            _, classes = package
            for j, c in enumerate(classes):
                self.packages[i][1][j] = self.__delete_before_last_dot(c)

    def __delete_before_last_dot(self, class_name: str) -> str:
        """
        Delete the string before the last dot.
        """
        return class_name.split('.')[-1] if '.' in class_name else class_name

    def _remove_special_characters(self) -> None:
        """
        Remove special characters from the class name.
        """
        for i, package in enumerate(self.packages):
            for j, c in enumerate(package[1]):
                self.packages[i][1][j] = re.sub(r'[^A-Za-z0-9\s]', '', c)

    def _remove_duplicates(self) -> None:
        """
        Remove duplicate class names, keeping only the first occurrence.
        """
        for i, package in enumerate(self.packages):
            _, classes = package
            filtered_classes = self.__list_without_duplicates(classes)
            self.packages[i][1] = filtered_classes

    def __list_without_duplicates(self, classes: list) -> list:
        """
        Remove duplicate class names, keeping only the first occurrence.
        """
        seen = set()
        filtered_classes = []

        for class_name in classes:
            if class_name not in seen:
                seen.add(class_name)
                filtered_classes.append(class_name)

        return filtered_classes

    def send(self) -> None:
        """
        Send the filtered packages to the next observer.
        """
        for package in self.packages:
            package_name, classes = package
            self.observer_to_send.on_package_found(
                package_name, classes)


class MethodsFilter(Filter):
    """
    Filter the Methods.
    """

    def __init__(self, methods: list, observer_to_send: Observer) -> None:
        super().__init__(observer_to_send, methods=methods)

    def filter(self) -> None:
        """
        Filter the methods:
        - Removing special characters of the methods names.
        """
        self._remove_special_characters()

    def _remove_special_characters(self) -> None:
        """
        Remove special characters from the methods name.
        """
        for i, method in enumerate(self.methods):
            self.methods[i][1]= re.sub(r'[^A-Za-z0-9\s]', '', method[1])

    def send(self) -> None:
        """
        Send the filtered methods to the next observer.
        """
        for method in self.methods:
            class_name, method_name = method
            self.observer_to_send.on_method_found(class_name, method_name)


def init_module(api: CddeAPI) -> None:
    """
    Initialize the module on the API.
    """
    api.register_puml_observer('filter', Filter)
