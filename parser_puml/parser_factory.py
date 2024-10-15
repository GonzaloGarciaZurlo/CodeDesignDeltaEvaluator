from parser_puml import puml_parser, regex_uml, puml_observer

# list of parsers
REGEX = "regex"

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
        else:   
            print("Invalid parser")