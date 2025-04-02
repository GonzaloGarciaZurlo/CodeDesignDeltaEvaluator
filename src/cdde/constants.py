"""
This file contains the constants used in the parser module.
"""
from .puml_observer import Relationship, ClassKind


def convert_relation(relation: str) -> tuple[Relationship, bool]:
    """
    function to convert relation symbols to names
    """
    relation_map = {
        '--': (Relationship.association, False),
        '--*': (Relationship.composition, False),
        '*--': (Relationship.composition, True),
        '--o': (Relationship.aggregation, False),
        'o--': (Relationship.aggregation, True),
        '-->': (Relationship.dependency, False),
        '<--': (Relationship.dependency, True),
        '..|>': (Relationship.implementation, False),
        '<|..': (Relationship.implementation, True),
        '--|>': (Relationship.inheritance, False),
        '<|--': (Relationship.inheritance, True)
    }
    return relation_map[relation]


def convert_class_kind(kind: str) -> ClassKind:
    """
    function to convert class kind symbols to names
    """
    kind_map = {
        'class': (ClassKind.Class),
        'interface': (ClassKind.Interface),
        'abstract class': (ClassKind.Abstract),
        'abstract': (ClassKind.Abstract)
    }
    return kind_map[kind]
