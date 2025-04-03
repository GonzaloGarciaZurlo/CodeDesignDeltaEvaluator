"""
This file contains the constants used in the parser module.
"""
from .puml_observer import Relationship, ClassKind


def convert_relation(relation: str) -> tuple[Relationship, bool]:
    """
    function to convert relation symbols to names
    """
    relation_map = {
        '--': (Relationship.ASSOCIATION, False),
        '--*': (Relationship.COMPOSITION, False),
        '*--': (Relationship.COMPOSITION, True),
        '--o': (Relationship.AGGREGATION, False),
        'o--': (Relationship.AGGREGATION, True),
        '-->': (Relationship.DEPENDENCY, False),
        '<--': (Relationship.DEPENDENCY, True),
        '..|>': (Relationship.IMPLEMENTATION, False),
        '<|..': (Relationship.IMPLEMENTATION, True),
        '--|>': (Relationship.INHERITANCE, False),
        '<|--': (Relationship.INHERITANCE, True)
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
