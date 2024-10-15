"""
This module handles user interaction, allowing the selection of the parser and observers to be used.
"""
from parser_puml import parser_factory, observer_factory


def console():
    """
    Handles user interaction, allowing the selection of the parser and observers to be used.
    """
    # Creacion de obsvers
    print("Select which observer you want to use:")
    print("printer")
    print("neo4j")
    print("composable")
    o = input()
    if o == "composable":
        print("Select which observers you want to use:")
        print("printer")
        print("neo4j")
        obs = input().split()
        obs_list = []
        for observer in obs:
            obs_list.append(
                observer_factory.ObserverFactory.create_observer(observer))
        composable = observer_factory.ObserverFactory.create_observer(
            "composable", obs_list)
        o = composable

    # Creacion de parser
    print("Select which parser you want to use:")
    print("regex")
    p = input()
    return parser_factory.ParserFactory.create_parser(p, o)
