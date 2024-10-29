"""
API for CodeDesignDeltaEvaluator
"""
from abc import ABC, abstractmethod
from overrides import override
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Type
from puml_generator import PumlGenerator
from puml_parser import PumlParser
from puml_observer import Observer
import os
from typing import Optional
import importlib


class CddeAPIAbstract(ABC):
    @abstractmethod
    def register_puml_generator(self, extension: str, generator: Type[PumlGenerator]) -> None:
        """
        Register a PlantUML generator.
        """
        pass

    def register_puml_parser(self, extension: str, parser: Type[PumlParser]) -> None:
        """
        Register a PlantUML parser.
        """
        pass

    def register_puml_observer(self, extension: str, observer: Type[Observer]) -> None:
        """
        Register a PlantUML observer.
        """
        pass


class CddeAPI(CddeAPIAbstract):
    """
    API for CodeDesignDeltaEvaluator
    """

    def __init__(self) -> None:
        self.generators: dict[str, Type[PumlGenerator]] = {}
        self.parsers: dict[str, Type[PumlParser]] = {}
        self.observers: dict[str, Type[Observer]] = {}

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
            raise ImportError(f"Cannot find module named '{name}' at path '{path}'")

        rule_module: ModuleType = importlib.util.module_from_spec(spec)
        os.sys.modules[unique_name] = rule_module

        if spec.loader is None:
            raise ImportError(f"Loader is not defined for module '{name}'")

        spec.loader.exec_module(rule_module)

        if hasattr(rule_module, 'init_module'):
            rule_module.init_module(self)
