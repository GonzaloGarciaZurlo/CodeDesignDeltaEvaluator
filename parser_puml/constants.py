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
DEPENDENCY = '-->'
COMPOSITION = '*--'
AGGREGATION = 'o--'
ASSOCIATION = '--'

# Mapping relation symbols to names
RELATION_MAP = {
    INHERITANCE: 'inheritance',
    INHERITANCE2: 'inheritance2',
    IMPLEMENTATION: 'implementation',
    DEPENDENCY: 'dependency',
    COMPOSITION: 'composition',
    AGGREGATION: 'aggregation',
    ASSOCIATION: 'association'
}

# Function to convert relation symbols to names
def convert_relation(relation):
    return RELATION_MAP.get(relation, relation)