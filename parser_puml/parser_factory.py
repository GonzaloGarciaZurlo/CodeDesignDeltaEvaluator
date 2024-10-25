"""
 Factory class that creates the parser object based on the selected implementation.
"""
from CodeDesignDeltaEvaluator.addons import parsimonius_parser
from CodeDesignDeltaEvaluator.factories import puml_observer, puml_parser
from CodeDesignDeltaEvaluator.addons import regex_uml

# list of parsers
REGEX = "regex"
PARSIMONIUS = "parsimonius"


class ParserFactory():
    """
    Class that creates the parser object based on the selected implementation.
    """

    @staticmethod
    def create_parser(name: str, obserber: puml_observer.Observer) -> puml_parser.PumlParser:
        """
        Creates the parser object based on the selected implementation.
        """
        if name == REGEX:
            return regex_uml.Regex(obserber)
        if name == PARSIMONIUS:
            return parsimonius_parser.Parsimonius(obserber)
        print("Invalid parser")
        return None
