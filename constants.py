"""
This file contains the constants used in the parser module.
"""

# Regex parser constants :
NAME_SPACE_PATTERN = r'namespace\s+([\w.]+)'
CLASS_PATTERN = r'(?<!abstract\s)\bclass\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|(?<!abstract\s)\bclass\s+([\w.]+)'
RELATION_PATTERN = r'''(["']?[\w.]+["']?)\s*(--\|>|<\|--|\.\.\|>|<\|\.{2}|-->|<--|\*--|--\*|o--|--o|--)\s*(["']?[\w.]+["']?)'''
ABS_CLASS_PATTERN = r'abstract class\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|abstract class\s+([\w.]+)'
ABS_PATTERN = r'abstract\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|abstract\s+([\w.]+)'

# Relation type constants
INHERITANCE = '--|>'
INHERITANCE2 = '<|--'
IMPLEMENTATION = '..|>'
IMPLEMENTATION2 = '<|..'
DEPENDENCY = '-->'
DEPENDENCY2 = '<--'
COMPOSITION = '*--'
COMPOSITION2 = '--*'
AGGREGATION = 'o--'
AGGREGATION2 = '--o'
ASSOCIATION = '--'

# Mapping relation symbols to names
RELATION_MAP = {
    INHERITANCE: 'inheritance',
    INHERITANCE2: 'inheritance',
    IMPLEMENTATION: 'implementation',
    IMPLEMENTATION2: 'implementation',
    DEPENDENCY: 'dependency',
    DEPENDENCY2: 'dependency',
    COMPOSITION: 'composition',
    COMPOSITION2: 'composition',
    AGGREGATION: 'aggregation',
    AGGREGATION2: 'aggregation',
    ASSOCIATION: 'association'
}

# Function to convert relation symbols to names


def convert_relation(relation):
    """
    function to convert relation symbols to names
    """
    return RELATION_MAP.get(relation, relation)
