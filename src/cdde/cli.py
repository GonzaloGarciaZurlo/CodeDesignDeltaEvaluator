"""
This module is the CLI of the tool.
It uses the Typer library to create the CLI. 
"""
from typing import List
from enum import StrEnum
import typer
from .main import Main

app = typer.Typer(name="CddE")

# CddE https://github.com/jfeliu007/goplantuml 168 --leng .go # GO (none changes)

# "https://github.com/jfeliu007/goplantuml", 145  # GO (many changes)


class Leng(StrEnum):
    """
    StrEnum for the language.
    """
    PY = ".py"
    GO = ".go"
    CPP = ".cpp"


class Store(StrEnum):
    """
    StrEnum for the database.
    """
    NEO4J = "Neo4j"


class FormatResult(StrEnum):
    """
    StrEnum for the format of the result.
    """
    JSON = "json"
    CSV = "csv"
    CONSOLE = "console"


def set_language(language: Leng, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if language is not None:
        main.set_language(language.value)


def add_yamls(yamls: list[str], main: Main) -> None:
    """
    Set the options of the tool.
    """
    for yaml_filepath in yamls:
        main.set_expr_evaluator(yaml_filepath)


def add_observer(observer: List[Store], main: Main) -> None:
    """
    Set the options of the tool.
    """
    for obs in observer:
        if obs is not None:
            main.set_observers(obs.value)


def add_visual_mode(visual: bool, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if visual:
        main.set_observers('printer')


def add_result_observer(result_observer: List[FormatResult],
                        main: Main) -> None:
    """
    Set the options of the tool.
    """
    for res_obs in result_observer:
        if res_obs is not None:
            if res_obs.value == "console":
                main.set_result_observers("res_printer")
            else:
                main.set_result_observers(res_obs.value)


@app.command()
def CddE(
        repo_git: str = typer.Argument(
            ..., help="Link to the repository to evaluate"),
        pr_number: int = typer.Argument(..., help="Pull request number"),
        yamls: List[str] = typer.Argument(
            ..., help="Select the file with the queries"),
        leng: Leng = typer.Option(Leng.PY.value,
                                  help="Select language of the repository"),
        store: List[Store] = typer.Option([Store.NEO4J],
                                          help="Select graph database"),
        visual: bool = typer.
    Option(
        False,
        "--visual",
        "--v",
        help=
        "Visualize the class and relations of the repository on the console"),
        format_result: List[FormatResult] = typer.Option(
            [FormatResult.JSON.value],
            help="Select the format of the result")):
    """Run the tool CddE"""
    main = Main()
    main.set_api()
    set_language(leng, main)
    add_yamls(yamls, main)
    add_observer(store, main)
    add_visual_mode(visual, main)
    add_result_observer(format_result, main)

    main.runCddE(repo_git, pr_number)
