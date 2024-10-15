"""
This file contains the constants used in the parser module.
"""

# Regex parser constants :
CLASS_PATTERN = r'class\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|class\s+([\w.]+)'
RELATION_PATTERN = r'(\w+[\w.]+)\s*([-\*<>|]+)\s*(\w+[\w.]+)'
ABS_CLASS_PATTERN = r'abstract\s+class\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|abstract\s+class\s+([\w.]+)'
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
    INHERITANCE2: 'inheritance2',
    IMPLEMENTATION: 'implementation',
    IMPLEMENTATION2: 'implementation2',
    DEPENDENCY: 'dependency',
    DEPENDENCY2: 'dependency2',
    COMPOSITION: 'composition',
    COMPOSITION2: 'composition2',
    AGGREGATION: 'aggregation',
    AGGREGATION2: 'aggregation2',
    ASSOCIATION: 'association'
}

# Function to convert relation symbols to names
def convert_relation(relation):
    """
    function to convert relation symbols to names
    """
    return RELATION_MAP.get(relation, relation)
