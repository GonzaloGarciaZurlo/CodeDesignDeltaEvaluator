"""
API for CodeDesignDeltaEvaluator
"""
from abc import ABC, abstractmethod
import importlib
from types import ModuleType
from typing import Type, Optional
from importlib.machinery import ModuleSpec
import os
import sys
from overrides import override
from puml_generator import PumlGenerator
from puml_parser import PumlParser
from puml_observer import Observer
from result_observer import ResultObserver
from result_queries import ResultQueries


class CddeAPIAbstract(ABC):
    """
    Abstract API for CodeDesignDeltaEvaluator
    """
    @abstractmethod
    def register_puml_generator(self, extension: str, generator: Type[PumlGenerator]) -> None:
        """
        Register a PlantUML generator.
        """

    def register_puml_parser(self, extension: str, parser: Type[PumlParser]) -> None:
        """
        Register a PlantUML parser.
        """

    def register_puml_observer(self, extension: str, observer: Type[Observer]) -> None:
        """
        Register a PlantUML observer.
        """

    def register_result_observer(self, extension: str, observer: Type[ResultObserver]) -> None:
        """
        Register a result observer.
        """

    def register_result_queries(self, extension: str, queries: Type[ResultQueries]) -> None:
        """
        Register result queries.
        """


class CddeAPI(CddeAPIAbstract):
    """
    API for CodeDesignDeltaEvaluator
    """

    def __init__(self) -> None:
        self.generators: dict[str, Type[PumlGenerator]] = {}
        self.parsers: dict[str, Type[PumlParser]] = {}
        self.observers: dict[str, Type[Observer]] = {}
        self.results_observers: dict[str, Type[ResultObserver]] = {}
        self.result_queries: dict[str, Type[ResultQueries]] = {}

    @override
    def register_puml_generator(self, extension: str, generator: Type[PumlGenerator]) -> None:
        """
        Register a PlantUML generator.
        """
        self.generators[extension] = generator

    @override
    def register_puml_parser(self, extension: str, parser: Type[PumlParser]) -> None:
        """
        Register a PlantUML parser.
        """
        self.parsers[extension] = parser

    @override
    def register_puml_observer(self, extension: str, observer: Type[Observer]) -> None:
        """
        Register a PlantUML observer.
        """
        self.observers[extension] = observer

    @override
    def register_result_observer(self, extension: str, observer: Type[ResultObserver]) -> None:
        """
        Register a result observer.
        """
        self.results_observers[extension] = observer

    @override
    def register_result_queries(self, extension: str, queries: Type[ResultQueries]) -> None:
        """
        Register result queries.
        """
        self.result_queries[extension] = queries

    def _generate_module_name(self, module: str) -> str:
        """
        Generate a unique module name.
        """
        return f"unique_{module}"

    def load_modules_from_directory(self, directory: str) -> None:
        """
        Load all modules from a given directory.
        """
        for filename in os.listdir(directory):
            if filename.endswith(".py"):
                module_path = os.path.join(directory, filename)
                module_name = os.path.splitext(filename)[0]
                self.load_module(module_path, module_name)

    def load_module(self, path: str, name: str) -> None:
        """
        Load a module from a given path.
        """
        unique_name = self._generate_module_name(name)
        spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(
            unique_name, path)
        if spec is None:
            raise ImportError(f"Cannot find module named '{
                              name}' at path '{path}'")

        rule_module: ModuleType = importlib.util.module_from_spec(spec)
        sys.modules[unique_name] = rule_module

        if spec.loader is None:
            raise ImportError(f"Loader is not defined for module '{name}'")

        spec.loader.exec_module(rule_module)

        if hasattr(rule_module, 'init_module'):
            rule_module.init_module(self)
