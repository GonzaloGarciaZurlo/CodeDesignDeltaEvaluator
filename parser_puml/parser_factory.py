from parser_puml import puml_parser


class ParserFactory():
    """
    Class that creates the parser object based on the selected implementation.
    """

    @staticmethod
    def create_parser(name: puml_parser.PumlParser):
        """
        Creates the parser object based on the selected implementation.
        """
        return name