# Regex parser constants :
CLASS_PATTERN = r'class\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|class\s+([\w.]+)'
RELATION_PATTERN = r'(\w+[\w.]+)\s*([-\*<>|]+)\s*(\w+[\w.]+)'
ABS_CLASS_PATTERN = r'abstract\s+class\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|abstract\s+class\s+([\w.]+)'
ABS_PATTERN = r'abstract\s+"?([\w\s]+)"?\s+as\s+([\w.]+)|abstract\s+([\w.]+)'
