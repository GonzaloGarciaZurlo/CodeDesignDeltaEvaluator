from parser_puml import puml_observer


class ObserverFactory():
    """
    Class that creates the parser object based on the selected implementation.
    """

    @staticmethod
    def create_observer(name: puml_observer.Observer) -> puml_observer.Observer:
        """
        Creates the parser object based on the selected implementation.
        """
        return name