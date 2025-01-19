"""
This module is the CLI of the tool.
It uses the Typer library to create the CLI. 
"""
import typer
from typing import List
from .main import Main
from enum import StrEnum


app = typer.Typer(name="CddE")

# "https://github.com/jfeliu007/goplantuml", 168  # GO (none changes)

# "https://github.com/jfeliu007/goplantuml", 145  # GO (many changes)


class Leng(StrEnum):
    """
    StrEnum for the lenguage.
    """
    py = ".py"
    go = ".go"
    cpp = ".cpp"


class Queryleng(StrEnum):
    """
    StrEnum for the query lenguage.
    """
    cypher = "cypher"


class Store(StrEnum):
    """
    StrEnum for the database.
    """
    Neo4j = "Neo4j"


class FormatResult(StrEnum):
    """
    StrEnum for the format of the result.
    """
    json = "json"
    csv = "csv"
    console = "console"


def set_lenguage(lenguage: Leng, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if lenguage is not None:
        main.set_lenguage(lenguage.value)


def set_querylenguage(querylenguage: Queryleng, main: Main) -> None:
    """
    Set the options of the tool.
    """
    if querylenguage is not None:
        main.set_queryl(querylenguage.value)


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


def add_result_observer(result_observer: List[FormatResult], main: Main) -> None:
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
    repo_git: str = typer.Argument(..., help="Link to the repository to evaluate"),
    pr_number: int = typer.Argument(..., help="Pull request number"),
    leng: Leng = typer.Option(
        ".py", help="Select lenguage of the repository"),
    queryl: Queryleng = typer.Option("cypher",
                                     help="Select query lenguage"),
    store: List[Store] = typer.Option(
        ["Neo4j"], help="Select graph database"),
    visual: bool = typer.Option(
        False, "--visual", "--v", help="Visualize the class and relations of the repository on the console"),
    format_result: List[FormatResult] = typer.Option(
        ["json"], help="Select the format of the result")
):
    """Run the tool CddE"""
    main = Main()
    main.set_api()
    set_lenguage(leng, main)
    set_querylenguage(queryl, main)
    add_observer(store, main)
    add_visual_mode(visual, main)
    add_result_observer(format_result, main)

    main.runCddE(repo_git, pr_number)


def main():
    app()


if __name__ == "__main__":
    app()
