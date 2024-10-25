"""
API for CodeDesignDeltaEvaluator
"""
from importlib.machinery import ModuleSpec
from types import ModuleType
from typing import Type
from CodeDesignDeltaEvaluator.factories.puml_generator import PumlGenerator
from factories.puml_parser import PumlParser
from factories.puml_observer import Observer
import os
from typing import Optional
import importlib


class CddeAPI():
    """
    API for CodeDesignDeltaEvaluator
    """

    def __init__(self) -> None:
        self.generators: dict[str, Type[PumlGenerator]]
        self.parsers: dict[str, Type[PumlParser]]
        self.observers: dict[str, Type[Observer]]
        self.register_puml_generator()
        self.register_puml_parser()
        self.register_puml_observer()

    def register_puml_generator(self, extension: str, generator: Type[PumlGenerator]) -> None:
        """
        Register a PlantUML generator.
        """
        self.generators[extension] = generator

    def register_puml_parser(self, extension: str, parser: Type[PumlParser]) -> None:
        """
        Register a PlantUML parser.
        """
        self.parsers[extension] = parser

    def register_puml_observer(self, extension: str, observer: Type[Observer]) -> None:
        """
        Register a PlantUML observer.
        """
        self.observers[extension] = observer


def _generate_module_name(module: str) -> str:
    # Implementa la lógica para generar un nombre único para el módulo
    return f"unique_{module}"


def _check_module(module: ModuleType) -> None:
    # Implementa la lógica para verificar el módulo
    if not hasattr(module, 'MODULE') or not hasattr(module, 'init_module'):
        raise print(f"Module {module} does not have required attributes")


def _load_extension(module: str):
    """Try to load a module"""
    unique_name = _generate_module_name(module)
    spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(
        unique_name, module)

    rule_module: ModuleType = importlib.util.module_from_spec(spec)
    os.sys.modules[unique_name] = rule_module

    spec.loader.exec_module(rule_module)

    new_extension = rule_module.MODULE
    _check_module(new_extension)

    return new_extension


def _set_up_extension(module: str) -> None:

    try:
        # Try to import the module as current package module
        _load_extension(module)

    # catch filenotfounderror
    except (FileNotFoundError) as _:
        # If exception, try to import the module as Abram package module
        relative_module: str = os.path.join(os.path.dirname(__file__), "addons",
                                            module)
        _load_extension(relative_module)

    #init_module()

_set_up_extension("MODULE") # ?


#MODULE = ?