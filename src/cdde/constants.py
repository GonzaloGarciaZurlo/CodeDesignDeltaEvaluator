"""
This file contains the constants used in the parser module.
"""
from enum import Enum, auto
from .puml_observer import Relationship, ClassKind, MethodKind


class Direction(Enum):
    """
    Enum class to represent the direction of a relationship.
    """
    RIGHT = auto()
    BACKWARD = auto()


def convert_relation(relation: str) -> tuple[Relationship, Direction]:
    """
    function to convert relation symbols to names
    """
    relation_map = {
        '--': (Relationship.ASSOCIATION, Direction.RIGHT),
        '--*': (Relationship.COMPOSITION, Direction.BACKWARD),
        '*--': (Relationship.COMPOSITION, Direction.RIGHT),
        '--o': (Relationship.AGGREGATION, Direction.BACKWARD),
        'o--': (Relationship.AGGREGATION, Direction.RIGHT),
        '-->': (Relationship.DEPENDENCY, Direction.BACKWARD),
        '<--': (Relationship.DEPENDENCY, Direction.RIGHT),
        '..|>': (Relationship.IMPLEMENTATION, Direction.BACKWARD),
        '<|..': (Relationship.IMPLEMENTATION, Direction.RIGHT),
        '--|>': (Relationship.INHERITANCE, Direction.BACKWARD),
        '<|--': (Relationship.INHERITANCE, Direction.RIGHT)
    }
    return relation_map[relation]


def convert_class_kind(kind: str) -> ClassKind:
    """
    function to convert class kind symbols to names
    """
    kind_map = {
        'class': (ClassKind.CLASS),
        'interface': (ClassKind.INTERFACE),
        'abstract class': (ClassKind.ABSTRACT),
        'abstract': (ClassKind.ABSTRACT)
    }
    return kind_map[kind]


def convert_visibility(vis: str) -> MethodKind:
    """
    Convert visibility symbols to names.
    """
    vis_map = {
        '+': MethodKind.PUBLIC,
        '-': MethodKind.PRIVATE,
        '#': MethodKind.PROTECTED,
        '': MethodKind.PUBLIC,
        '_': MethodKind.PRIVATE,
        '__': MethodKind.PROTECTED
    }
    # Default to public if not found
    return vis_map.get(vis, MethodKind.PUBLIC)
